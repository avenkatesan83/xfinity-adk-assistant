import globals
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from utils.adkrunnerutils import initialize_runner, MissingAPIKeyError, MissingAgentEngineIdError
from api.router.agent_router import agent_router
from contextlib import asynccontextmanager
from utils.modelarmorutils import initialize_model_armor_client
from utils.datastoreutils import initialize_datastore_client
from utils.vertextaiutils import initialize_vertexai_client

# --- Configuration and Initialization ---

load_dotenv()
print("✅ Environment variables loaded.")

def load_globals():
    """
    Loads global configuration variables from environment variables and assigns them to the globals module.

    Environment Variables:
        PROJECT_ID: The Google Cloud project ID.
        LOCATION_ID: The location or region identifier.
        TEMPLATE_ID: The template identifier.

    Each variable is set to an empty string if the corresponding environment variable is not found.
    """
    """Loads global configuration variables from environment variables."""
    globals.google_vertexai_use_vertexai = os.getenv("GOOGLE_GENAI_USE_VERTEXAI")
    globals.google_api_key = os.getenv("GOOGLE_API_KEY", "")
    globals.project_id = os.getenv("PROJECT_ID", "")
    globals.location_id = os.getenv("LOCATION_ID", "")
    globals.agent_engine_id = os.getenv("VERTEX_AGENT_ENGINE_ID", "")
    globals.discovery_engine_api_endpoint = os.getenv("DISCOVERY_ENGINE_API_ENDPOINT", "")
    globals.template_id = os.getenv("TEMPLATE_ID", "")
    globals.model_armor_api_endpoint_uri = f"modelarmor.{globals.location_id}.rep.googleapis.com"
    globals.faq_data_store_id = os.getenv("FAQ_DATA_STORE_ID", "")

# --- FastAPI Lifecycle Hook using Lifespan ---

# NOTE: We define the lifespan function first, then create the app instance once.

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initializes the Agent Runner when the FastAPI application starts."""

    try:
        load_globals()
        print("✅ Global configuration loaded.")
        
        print("\n🚀 Initializng Model Armor Client...")
        initialize_model_armor_client()
        print("✅ Model Armor Client initialized.")
        print("\n🚀 Initializing Vertex AI Client...")
        initialize_vertexai_client()
        print("✅ Vertex AI Client initialized.")
        print("\n🚀 Initializing Datastore Client...")
        initialize_datastore_client()
        print("✅ Datastore Client initialized.")
        print("\n🚀 Initializing ADK Agent Runner...")
        await initialize_runner()
        print("✅ Runner is ready.")
    
    except MissingAPIKeyError as e:
        # Handles missing API key for the Agent Runner
        print(f"❌ Initialization Error: {e}")
        raise RuntimeError("Agent setup failed due to missing API key credentials.") from e
    except MissingAgentEngineIdError as e:
        # Handles missing API key for the Agent Runner
        print(f"❌ Initialization Error: {e}")
        raise RuntimeError("Agent setup failed due to missing Agent Engine Id.") from e
    except Exception as e:
        # Catch-all for other initialization errors
        print(f"❌ Unknown Initialization Error: {e}")
        raise RuntimeError("Agent setup failed due to an unexpected error.") from e

    # Yield control back to FastAPI to start serving requests
    yield
    
    # Cleanup phase (runs on shutdown)
    print("Application shutdown complete.")


# --- Redefine the FastAPI application instance to use the lifespan context manager ---
app = FastAPI(
    title="ADK Agent Demo API", 
    description="Exposes the Gemini ADK Xfinity Assistant via a REST endpoint.",
    lifespan=lifespan # Attach the lifecycle hook here
)

# --- Include all routers in the main application ---
app.include_router(agent_router)