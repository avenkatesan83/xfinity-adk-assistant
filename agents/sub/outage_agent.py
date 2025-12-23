from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.genai import types
import globals

retry_config=types.HttpRetryOptions(
    attempts=5,  # Maximum retry attempts
    exp_base=7,  # Delay multiplier
    initial_delay=1, # Initial delay before first retry (in seconds)
    http_status_codes=[429, 500, 503, 504] # Retry on these HTTP errors
)

def create_agent() -> Agent:

    # Authroizer Agent: Handles the user authorization
    authorizer_agent = Agent(
        name="AuthorizerAgent",
        model=Gemini(
            model=globals.llm_model_name,
            retry_options=retry_config
        ),
        description="An authorizer agent to handle user authorization.",
        instruction="""You're a specialized agent that handles user authorization. Your primary function is,
        Prompt the user for their member ID.
        1. **Authorizing a User:**
≈           - Once you have the member ID, you MUST verify if the user is authorized to access the system.
                - Use tool `validate_member_id` to validate the member ID.
                    - After verification, 
                        - If the user is authorized, you MUST inform the user of their authorization status.
                        - If the user is not authorized,
                            - you MUST inform the user that they are not authorized to access the system and terminate the conversation politely.        """,
        output_key="authorizer_output",  # The result of this agent will be stored in the session state with this key.
        tools=[validate_member_id]
    )

    print("✅ Outage Agent created.")
    return authorizer_agent


def validate_member_id(member_id: str) -> bool:
    """Validates the member ID."""
    return member_id == "venky-123"