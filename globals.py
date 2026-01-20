from google.adk.runners import Runner, InMemoryRunner
from google.adk.sessions import InMemorySessionService, VertexAiSessionService
from google.adk.memory import VertexAiMemoryBankService
from google.genai import types
from google.cloud import modelarmor_v1
from google.cloud import discoveryengine_v1
import vertexai

# -- ADK related globals --
app_name: str = "Xfinity ADK Agent Demo"
welcome_event: str = "WELCOME_EVENT"

# Initialize the global runner variable to None. 
# It will be set later in main.py's startup event.
#global_runner: InMemoryRunner = None
global_runner: Runner = None
#session_service: InMemorySessionService = None
session_service: VertexAiSessionService = None
memory_service: VertexAiMemoryBankService = None

# -- Google Vertex AI related globals --
vertex_client: vertexai = None
agent_engine_id: str = None
google_vertexai_use_vertexai: str = None
agent_engine_location_id: str = "us-central1"
google_api_key: str = None
llm_model_name: str = "gemini-2.5-flash-lite"
user_data: dict = {}

# -- Agent retry config globals --
retry_config=types.HttpRetryOptions(
    attempts=5,  # Maximum retry attempts
    exp_base=7,  # Delay multiplier
    initial_delay=1, # Initial delay before first retry (in seconds)
    http_status_codes=[429, 500, 503, 504] # Retry on these HTTP errors
)

# -- Model armor related globals --
project_id: str = None
location_id: str = None
template_id: str = None
model_armor_api_endpoint_uri: str = None
model_armor_client_transport: str = "rest"
model_armor_client: modelarmor_v1.ModelArmorClient = None

# -- Data Store related globals --
faq_data_store_id: str = None
discovery_engine_api_endpoint: str = None
datastore_client: discoveryengine_v1 = None

# -- Default user prompt globals --
default_user_prompt: str = "Hi"

# -- MCP related globals --
mcp_server_url: str = None

# -- A2A agent related globals --
agent_card_well_known_path: str = None
a2a_agent_server_url: str = None