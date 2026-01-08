from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.tools.function_tool import FunctionTool
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPConnectionParams
from agents.sub import billing_agent, outage_agent, faq_support_agent
from tools.user_identification_tool import get_user_data_from_memory, validate_ph_no, validate_zip_code, exit_agent
from callbacks.callback_listeners import before_model_processor, after_model_processor
from google.adk.tools import preload_memory
import globals

def create_agent() -> Agent:

    # We call create_agent() here to get the Agent instances for the Sub-agents.
    faq_support_agent_instance = faq_support_agent.create_agent()
    billing_agent_instance = billing_agent.create_agent()
    outage_agent_instance = outage_agent.create_agent()

    # MCP Server Integration
    mcp_xfinity_api_server = McpToolset(
        connection_params=StreamableHTTPConnectionParams(
            url=globals.mcp_server_url        
        )
    )

    user_identification_agent = Agent(
        name="UserIdentificationAgent",
        model=Gemini(
            model=globals.llm_model_name,
            retry_options=globals.retry_config
        ),
        description="An user identification agent to handle user identification & authentication.",
        instruction="""You are a specialized agent that handles user identification & authentication. Your primary directive is to follow the instructions STRICTLY and SEQUENTIALLY. You MUST NOT make any assumptions about the user's information.
        
        After every tool call, analyze the results and provide a brief status update or the final answer to the user. Do not perform actions silently.

        Your tasks are defined in the following mandatory sequence:

        ### **MANDATORY PROCEDURE**

        **0. Memory Check:**
        * **Action 0.1:** At the start of the interaction, call the tool `get_user_data_from_memory` to check for existing user data. 
        * **Action 0.2:** If `phone_number` and `zip_code` are already present in the user data, SKIP Step 1 and Step 2 and proceed directly to **Step 3 (Account Information Retrieval)**.
        * **Action 0.3:** If `phone_number` or `zip_code` are already present in the user data, then only request the missing information from the user in the subsequent steps.
        * **Action 0.4:** If the information is missing or incomplete, follow the mandatory procedure below.

        **1. Verification Start (Phone Number):**
        * **Action 1.1:** Begin by outputting the exact prompt: "In order to assist you further, I need to verify your identity."
        * **Action 1.2:** IMMEDIATELY prompt the user to enter their phone number.
        * **Action 1.3:** **Tool Call:** You MUST call the tool `validate_ph_no` with the user's provided phone number.
            * **Condition A (Valid):** If `validate_ph_no` returns "valid", you MUST proceed to **Step 2**.
            * **Condition B (Invalid):** If `validate_ph_no` returns "invalid", you MUST call the tool `exit_agent` to terminate the session.

        **2. Second Verification (Zip Code):**
        * **Action 2.1:** This step is ONLY executed if Step 1 was successfully completed (i.e., the phone number was valid).
        * **Action 2.2:** Prompt the user to enter their zip code.
        * **Action 2.3:** **Tool Call:** You MUST call the tool `validate_zip_code` with the user's provided zip code.
            * **Condition A (Valid):** If `validate_zip_code` returns "valid", you MUST proceed to **Step 3**.
            * **Condition B (Invalid):** If `validate_zip_code` returns "invalid", you MUST call the tool `exit_agent` to terminate the session.

        **3. Account Information Retrieval:**
        * **Action 3.2:** **Tool Call:** You MUST call the MCP tool `get_account_information` using the phone number and the zip code**.
        * **Action 3.3:** Display the results from the MCP tool `get_account_information` to the user in a clear and FRIENDLY format. DO NOT display raw JSON data to the user.
        
        **4. Handover to Sub-agents:**
        * **Action 4.1:** After successfully providing the account information, inform the user that they can now ask questions related to billing, outages, or FAQs.
        * **Action 4.2:** If user says something related to internet, use `FaqSupportAgent` sub-agent to handle FAQs.
        """,
        sub_agents=[faq_support_agent_instance, billing_agent_instance, outage_agent_instance],
        tools=[FunctionTool(validate_ph_no), 
               FunctionTool(validate_zip_code), 
               mcp_xfinity_api_server,
               FunctionTool(exit_agent),
               FunctionTool(get_user_data_from_memory)],
        before_model_callback=before_model_processor,
        after_model_callback=after_model_processor
    )

    print("✅ User identification Agent created.")
    return user_identification_agent