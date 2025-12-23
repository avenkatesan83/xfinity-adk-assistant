from typing import Optional
from google.adk.agents.callback_context import CallbackContext
from google.adk.models import LlmRequest, LlmResponse
from google.genai import types
from guardrails.sanitizer import sanitize_user_prompt, sanitize_model_response

def after_model_processor(
    callback_context: CallbackContext, llm_response: LlmResponse
):
    """
    Logs the agent name and the first part of the LLM response text after model processing.

    Args:
        callback_context (CallbackContext): The context containing information about the agent.
        llm_response (LlmResponse): The response object returned by the LLM.

    This function prints the agent's name and the first part of the LLM response content for debugging or logging purposes.
    """

    """Log the LLM response"""
    agent_name = callback_context.agent_name
    print("[Callback] After model call...")
    print(f"[Callback] agent name: {agent_name}")

    # Inspect the response content
    response_text = ""
    if llm_response.content and llm_response.content.parts:
        response_text = llm_response.content.parts[0].text or ""
    print(f"[Callback] Llm model response: '{response_text}'")

    # Sanitize model response
    if response_text:
        sanitize_model_response(response_text)
    else:
        print("[Callback] No model response to sanitize.")

def before_model_processor( 
    callback_context: CallbackContext, llm_request: LlmRequest
) -> Optional[LlmResponse]:
    """
    Callback function to process and potentially intercept LLM requests before they are sent to the model.

    This function logs the agent name and the last user message from the LLM request. If the last user message contains the keyword "BLOCK" (case-insensitive), it returns a custom `LlmResponse` to skip the actual LLM call and provides a blocking message. Otherwise, it allows the request to proceed to the LLM by returning `None`.

    Args:
        callback_context (CallbackContext): The context object containing metadata about the agent and callback.
        llm_request (LlmRequest): The request object containing the conversation contents.

    Returns:
        Optional[LlmResponse]: A custom response to block the LLM call if the "BLOCK" keyword is detected, or `None` to proceed with the LLM call.
    """

    """Log the LLM request"""
    agent_name = callback_context.agent_name
    print("[Callback] Before model call...")
    print(f"[Callback] agent name: {agent_name}")

    # Inspect the last user message in the request contents
    last_user_message = ""
    if llm_request.contents and llm_request.contents[-1].role == 'user':
         if llm_request.contents[-1].parts:
            last_user_message = llm_request.contents[-1].parts[0].text
    print(f"[Callback] last user message: '{last_user_message}'")

    # Sanitize user prompt
    if last_user_message:
        sanitize_user_prompt(last_user_message)
    else:
        print("[Callback] No user message to sanitize.")

    # --- Skip Example ---
    # Check if the last user message contains "BLOCK"
    if last_user_message:
        if "BLOCK" in last_user_message.upper():
            print("[Callback] 'BLOCK' keyword found. Skipping LLM call.")
            # Return an LlmResponse to skip the actual LLM call
            return LlmResponse(
                content=types.Content(
                    role="model",
                    parts=[types.Part(text="LLM call was blocked by before_model_callback.")],
                )
            )
    else:
        print("[Callback] Proceeding with LLM call.")
        # Return None to allow the (modified) request to go to the LLM
        return None