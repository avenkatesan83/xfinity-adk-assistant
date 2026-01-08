import globals
import vertexai
import time


def initialize_vertexai_client() -> None:
    """
    Initializes and returns a Vertex AI client.

    This function creates a Vertex AI client using the project ID and agent engine location ID from the global variables.
    The client is used to interact with the Vertex AI services.

    Returns:
        None

    Raises:
        ValueError: If the project ID or agent engine location ID is not set in the global variables.

    Examples:
        >>> initialize_vertexai_client()
        Vertex AI client initialized.

    """

    try:
        vertex_client = vertexai.Client(
            project=globals.project_id,
            location=globals.agent_engine_location_id
            )
    
        globals.vertex_client = vertex_client

    except Exception as e:
        print(f"Error initializing Vertex AI client: {e}")


def create_agent_engine() -> None:
    # Use the standard model string for embeddings
    # common: text-embedding-004 or textembedding-gecko@003
    embedding_model_resource = "projects/gen-lang-client-0842450978/locations/us-central1/publishers/google/models/gemini-embedding-001"
    llm_model_name = "projects/gen-lang-client-0842450978/locations/us-central1/publishers/google/models/gemini-2.5-flash"

    # Define the memory bank configuration
    # Note: Structure varies slightly by SDK version; 
    # check if your version uses 'memory_bank_config' or 'vector_search_config'
    memory_bank_config = {
        "similarity_search_config": {
            "embedding_model": embedding_model_resource
        },
        "generation_config": {
            "model": llm_model_name,
      }
    }

    try:
        agent_engine = globals.vertex_client.agent_engines.create(
            config={
                "context_spec": {
                    "memory_bank_config": memory_bank_config
                }
            }
        )
        print(f"✅ Agent engine created: {agent_engine.api_resource.name.split('/')[-1]}")
    except Exception as e:
        print(f"❌ Failed to create agent engine: {e}")

def delete_all_agent_engines():
    engines = globals.vertex_client.agent_engines.list()
    
    if not engines:
        print("No engines found to delete.")
        return

    for engine in engines:
        engine_name = engine.api_resource.name
        try:
            print(f"Deleting engine: {engine_name}...")
            globals.vertex_client.agent_engines.delete(force=True, name=engine_name)
            print(f"✅ Deleted {engine_name}")
            
            # Wait 7 seconds between deletes to avoid the 10-per-minute limit
            print("Waiting 7 seconds to respect API quota...")
            time.sleep(7) 
            
        except Exception as e:
            print(f"❌ Failed to delete {engine_name}: {e}")

# In your __main__ block, just call:
# delete_all_agent_engines()
    
def main() -> None:
    """
    Main function to demonstrate the usage of the Vertex AI client.

    This function initializes the Vertex AI client and prints a message.

    Returns:
        None

    """
    initialize_vertexai_client()
    print("Vertex AI client successfully initialized.")
    create_agent_engine()
    #delete_all_agent_engines()

if __name__ == "__main__":
    main()