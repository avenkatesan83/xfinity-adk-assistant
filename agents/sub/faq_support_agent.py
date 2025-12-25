from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from utils.datastoreutils import search_in_datastore
import re
import globals

def search_faq_datastore(query: str) -> dict:
    """
    Searches the FAQ Datastore using the provided query string and returns relevant information.
    This function interacts with the Google Discovery Engine SearchServiceClient to perform a search
    against a specified FAQ datastore. It constructs a search request with content search specifications,
    including snippet and summary extraction. The function processes the search response to extract
    summaries or text snippets from the results, cleans any HTML tags from the snippets, and returns
    the most relevant information found.
    Args:
        query (str): The search query string to look up in the FAQ datastore.
    Returns:
        dict: A dictionary with a single key 'responseText' containing either the summary text,
              concatenated snippets, or a message indicating no relevant information was found.
              In case of errors, returns a string describing the error.
    """
    

    print(f"Searching FAQ Datastore with query: {query}")
    
    try:
        response = search_in_datastore(query)
        results = []
        print(response)
        # Check if there's a summary
        if hasattr(response, 'summary') and response.summary:
            print(f"Found summary: {response.summary.summary_text}")
            if response.summary.summary_text:
                return {"responseText": response.summary.summary_text}
        
        # Otherwise extract from results
        result_count = 0
        for result in response.results:
            result_count += 1
            doc = result.document
            
            # Access derived_struct_data
            if hasattr(doc, 'derived_struct_data') and doc.derived_struct_data:
                # Convert Protobuf Struct to Python Dict for easier access
                data = dict(doc.derived_struct_data)
                
                # TARGET: The 'snippets' key which is a List of Dicts
                if 'snippets' in data:
                    for s_obj in data['snippets']:
                        # The actual text is inside the 'snippet' key of the object
                        if 'snippet' in s_obj:
                            raw_text = s_obj['snippet']
                            # Optional: Clean HTML tags like <b> using regex
                            clean_text = re.sub('<[^<]+?>', '', raw_text)
                            results.append(clean_text)

        print(f"Processed {result_count} documents. Extracted {len(results)} snippets.")
        print(f"Search results: {results}")
        
        if results:
            return {"responseText": "\n\n".join(results)}
        else:
            return {"responseText": "No relevant information found in the knowledge base."}
            
    except Exception as e:
        error_msg = str(e)
        print(f"Error during search: {error_msg}")
        return f"Error searching datastore: {error_msg}"

def create_agent() -> Agent:
    faq_support_agent = Agent(
        name="FAQSupportAgent",
        model=Gemini(
            model=globals.llm_model_name,
            retry_options=globals.retry_config
        ),
        description="Answers questions using a specific Vertex AI Search datastore.",
        instruction="""You are a helpful assistant that answers questions about Xfinity services.
        Use the `search_faq_datastore` tool to find relevant information from the knowledge base.
        Provide clear, concise answers based on the search results attribute `responseText`.
        If no relevant information is found, politely tell the user you couldn't find the answer.
        """,
        tools=[search_faq_datastore]
    )

    print("✅ FAQ Support Agent created.")
    return faq_support_agent