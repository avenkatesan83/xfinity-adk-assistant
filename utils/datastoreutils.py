from google.api_core.client_options import ClientOptions
from google.cloud import discoveryengine_v1
import globals

def initialize_datastore_client() -> discoveryengine_v1:
    """
    Creates and returns a SearchServiceClient for interacting with Google Cloud's Discovery Engine API.

    Returns:
        discoveryengine
    """
    
    # Create client with proper endpoint
    client_options = ClientOptions(
        api_endpoint=globals.discovery_engine_api_endpoint
    )
    globals.datastore_client = discoveryengine_v1.SearchServiceClient(client_options=client_options)

def search_in_datastore(query: str) -> dict:
    """
    Searches the Datastore using the provided query string and returns relevant information.
    This function interacts with the Google Cloud's Discovery Engine SearchServiceClient to perform a search
    against a specified Datastore. It constructs a search request with content search specifications,
    including snippet and summary extraction. The function processes the search response to extract
    summaries or text snippets from the results, cleans any HTML tags from the snippets, and returns
    the most relevant information found.
    Args:
        query (str): The search query string to look up in the Datastore.
    Returns:
        dict: A dictionary with a single key 'responseText' containing either the summary text,
              concatenated snippets, or a message indicating no relevant information was found.
              In case of errors, returns a string describing the error.
    """
    # Construct the serving config path - note: use the FULL resource name format
    serving_config = (
        f"projects/{globals.project_id}/"
        "locations/global/"
        "collections/default_collection/"
        f"dataStores/{globals.faq_data_store_id}/"
        "servingConfigs/default_config"
    )
    
    print(f"Using serving_config: {serving_config}")
    
    try:
        # Create the search request with content search spec
        request = discoveryengine_v1.SearchRequest(
            serving_config=serving_config,
            query=query,
            page_size=5,
            content_search_spec=discoveryengine_v1.SearchRequest.ContentSearchSpec(
                snippet_spec=discoveryengine_v1.SearchRequest.ContentSearchSpec.SnippetSpec(
                    return_snippet=True,
                    max_snippet_count=3
                ),
                summary_spec=discoveryengine_v1.SearchRequest.ContentSearchSpec.SummarySpec(
                    summary_result_count=3,
                    include_citations=True
                )
            )
        )
        
        response = globals.datastore_client.search(request)
        return response
    except Exception as e:
        print(f"Error searching in Datastore: {e}")
        return {"responseText": f"Error searching in Datastore: {e}"}