from google.cloud import modelarmor_v1
from google.api_core.client_options import ClientOptions
import globals

def create_model_armor_client() -> modelarmor_v1.ModelArmorClient:
    """
    Creates and returns a ModelArmorClient for interacting with Google Cloud's Model Armor API.

    Returns:
        modelarmor_v1.ModelArmorClient: An instance of the ModelArmorClient configured with REST transport
        and the appropriate API endpoint.
    """
    try:
        client_options = ClientOptions(
            api_endpoint=globals.model_armor_api_endpoint_uri
        )
        model_armor_client = modelarmor_v1.ModelArmorClient(
            transport=globals.model_armor_client_transport,
            client_options=client_options,
        )
        return model_armor_client
    except Exception as e:
        print(f"[Error] Failed to create Model Armor client: {e}")
        raise