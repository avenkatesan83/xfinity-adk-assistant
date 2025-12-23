from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.runners import Runner, InMemoryRunner
from google.adk.sessions import InMemorySessionService, VertexAiSessionService
from callbacks.callback_listeners import before_model_processor, after_model_processor
from agents.sub import user_identification_agent
from google.adk.memory import VertexAiMemoryBankService
import vertexai
import globals

print("✅ ADK components imported successfully.")

class MissingAPIKeyError(Exception):
    """Exception for missing API key."""
    pass

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
        description="You're a customer support assistant `Xfinity Assistant` to gree the user. Be polite and empathetic.",
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

# ... (initialize_runner remains the same) ...

"""def initialize_runner() -> InMemoryRunner:
    #Initializes and returns the InMemoryRunner for the agent.
    
    # Check for credentials before initializing the runner
    if not globals.google_vertexai_use_vertexai == "TRUE":
        if not globals.google_api_key:
            raise MissingAPIKeyError(
                "GOOGLE_API_KEY environment variable not set and GOOGLE_GENAI_USE_VERTEXAI is not TRUE."
            )

    customer_support_agent = create_agent()
    runner = InMemoryRunner(agent=customer_support_agent)
    print("✅ ADK Runner initialized.")
    return runner
"""

async def initialize_runner() -> Runner:
    """Initializes and returns the Runner for the agent."""
    
    # Check for credentials before initializing the runner
    if not globals.google_vertexai_use_vertexai == "TRUE":
        if not globals.google_api_key:
            raise MissingAPIKeyError(
                "GOOGLE_API_KEY environment variable not set and GOOGLE_GENAI_USE_VERTEXAI is not TRUE."
            )


    vertex_client = vertexai.Client(
        project=globals.project_id,
        location=globals.agent_engine_location_id
        )
    # If you don't have an Agent Engine instance already, create an Agent Engine
    # Memory Bank instance using the default configuration.
    agent_engine = vertex_client.agent_engines.create()

    # Optionally, print out the Agent Engine resource name. You will need the
    # resource name to interact with your Agent Engine instance later on.
    print(f"Agent Engine resource name: {agent_engine.api_resource.name}")

    globals.agent_engine_id = agent_engine.api_resource.name.split("/")[-1]
    print(f"Agent Engine ID: {globals.agent_engine_id}")

    globals.memory_service = VertexAiMemoryBankService(
        project=globals.project_id,
        location=globals.agent_engine_location_id,
        agent_engine_id=globals.agent_engine_id
    )





    customer_support_agent = create_agent()

    # Use the below only for prototyping (InMemorySessionService)
    #globals.session_service = InMemorySessionService()

    # Use the below only for Production grade (VertexAiSessionService)
    globals.session_service = VertexAiSessionService(
        project=globals.project_id,
        location=globals.agent_engine_location_id,
        agent_engine_id=globals.agent_engine_id
    )
    runner = Runner(
        agent=customer_support_agent,
        app_name=globals.app_name,
        session_service=globals.session_service,
        memory_service=globals.memory_service
        )
    print("✅ ADK Runner initialized with VertexAISessionService.")
    return runner