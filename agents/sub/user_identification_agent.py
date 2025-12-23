from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.tools.function_tool import FunctionTool
from agents.sub import billing_agent, outage_agent, faq_support_agent
from tools.user_identification_tool import validate_ph_no, validate_zip_code, get_account_information, exit_agent
from callbacks.callback_listeners import before_model_processor, after_model_processor
import globals

def create_agent() -> Agent:

    # We call create_agent() here to get the Agent instances for the Sub-agents.
    faq_support_agent_instance = faq_support_agent.create_agent()
    billing_agent_instance = billing_agent.create_agent()
    outage_agent_instance = outage_agent.create_agent()

    user_identification_agent = Agent(
        name="UserIdentificationAgent",
        model=Gemini(
            model=globals.llm_model_name,
            retry_options=globals.retry_config
        ),
        description="An user identification agent to handle user identification & authentication.",
        instruction="""You are a specialized agent that handles user identification & authentication. Your primary directive is to follow the instructions STRICTLY and SEQUENTIALLY. You MUST NOT skip any step or make any assumptions about the user's information.
        
        After every tool call, analyze the results and provide a brief status update or the final answer to the user. Do not perform actions silently.

        Your tasks are defined in the following mandatory sequence:

        ### **MANDATORY PROCEDURE**

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
        * **Action 3.1:** This step is ONLY executed if both Step 1 and Step 2 were successfully completed.
        * **Action 3.2:** **Tool Call:** You MUST call the tool `get_account_information` using the **validated phone number and the validated zip code**.
        * **Action 3.3:** Display the results from `get_account_information` to the user in a clear and FRIENDLY format. DO NOT display raw JSON data to the user.
        
        **4. Handover to Sub-agents:**
        * **Action 4.1:** After successfully providing the account information, inform the user that they can now ask questions related to billing, outages, or FAQs.
        * **Action 4.2:** If user says something related to internet, use `FaqSupportAgent` sub-agent to handle FAQs.
        """,
        sub_agents=[faq_support_agent_instance, billing_agent_instance, outage_agent_instance],
        tools=[FunctionTool(validate_ph_no), 
               FunctionTool(validate_zip_code), 
               FunctionTool(get_account_information),
               FunctionTool(exit_agent)],
        before_model_callback=before_model_processor,
        after_model_callback=after_model_processor
    )

    print("✅ User identification Agent created.")
    return user_identification_agent