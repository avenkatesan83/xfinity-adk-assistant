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

    agent_engine = globals.vertex_client.agent_engines.create()
    print(f"\n\n✅ Your agent engine is created and agent engine id : {agent_engine.api_resource.name.split('/')[-1]}.\n\n")

def delete_all_agent_engines():
    engines = globals.vertex_client.agent_engines.list()
    
    if not engines:
        print("No engines found to delete.")
        return

    for engine in engines:
        engine_name = engine.api_resource.name
        try:
            print(f"Deleting engine: {engine_name}...")
            globals.vertex_client.agent_engines.delete(name=engine_name)
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