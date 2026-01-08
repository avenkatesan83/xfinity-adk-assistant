from google.adk.runners import Runner
from google.adk.sessions import VertexAiSessionService
from google.adk.plugins import LoggingPlugin 
from agents.root.customer_support_agent import create_agent
from google.adk.memory import VertexAiMemoryBankService
import globals

class MissingAPIKeyError(Exception):
    """Exception for missing API key."""
    pass

class MissingAgentEngineIdError(Exception):
    """Exception for missing Agent Engine Id."""
    pass

async def initialize_runner() -> None:
    """Initializes and returns the Runner for the agent."""
    
    # Check for credentials before initializing the runner
    if not globals.google_vertexai_use_vertexai == "TRUE":
        if not globals.google_api_key:
            raise MissingAPIKeyError(
                "GOOGLE_API_KEY environment variable not set and GOOGLE_GENAI_USE_VERTEXAI is not TRUE."
            )
        
    if not globals.agent_engine_id:
        raise MissingAgentEngineIdError(
            "AGENT_ENGINE_ID environment variable not set."
        )
        
    # If you don't have an Agent Engine instance already, create an Agent Engine
    """agent_engine = globals.vertex_client.agent_engines.create()
    print(f"Agent Engine resource name: {agent_engine.api_resource.name}")
    globals.agent_engine_id = agent_engine.api_resource.name.split("/")[-1]"""
    print(f"Agent Engine ID: {globals.agent_engine_id}")

    globals.memory_service = VertexAiMemoryBankService(
        project=globals.project_id,
        location=globals.agent_engine_location_id,
        agent_engine_id=globals.agent_engine_id
    )

    # Initialize the root agent
    customer_support_agent = create_agent()

    # Use the below only for prototyping (InMemorySessionService)
    #globals.session_service = InMemorySessionService()

    # Use the below only for Production grade (VertexAiSessionService)
    globals.session_service = VertexAiSessionService(
        project=globals.project_id,
        location=globals.agent_engine_location_id,
        agent_engine_id=globals.agent_engine_id
    )
    globals.global_runner = Runner(
        agent=customer_support_agent,
        app_name=globals.app_name,
        session_service=globals.session_service,
        memory_service=globals.memory_service,
        plugins=[LoggingPlugin()]
        )
    print("✅ ADK Runner initialized with VertexAISessionService & VertexAIMemoryBankService.")