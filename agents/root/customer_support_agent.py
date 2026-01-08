from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from callbacks.callback_listeners import before_model_processor, after_model_processor
from agents.sub import user_identification_agent
import globals

print("✅ ADK components imported successfully.")

def create_agent() -> Agent:
    """
    Constructs and returns a ADK agent for Customer Support.
    
    Returns:
        Agent: The configured root agent instance.
    """

    # We call create_agent() here to get the Agent instances for the Sub-agents.
    user_identification_agent_instance = user_identification_agent.create_agent()

    customer_support_agent = Agent(
        name="customer_support_assistant",
        description="You're a customer support assistant `Xfinity Assistant` to greet the user. Be polite and empathetic.",
        model=Gemini(
            model=globals.llm_model_name,
            retry_options=globals.retry_config
        ),
        instruction="""
            You are a helpful customer support assistant (Xfinity Assistant). Your primary function is to greet the user.
            
            Greet the user with "Hello! I'm your Xfinity assistant. I can help you with billing & outage related queries."

            After greeting the user, hand off the conversation to the `UserIdentificationAgent` sub-agent to handle user identification & authentication.
            """,
        sub_agents=[user_identification_agent_instance],
        before_model_callback=before_model_processor, # Assign the function here
        after_model_callback=after_model_processor # Assign the function here
    )

    print("✅ Customer Support Agent created.")
    return customer_support_agent