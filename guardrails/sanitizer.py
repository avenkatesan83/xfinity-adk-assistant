from google.cloud import modelarmor_v1
import globals

def sanitize_user_prompt(user_prompt) -> modelarmor_v1.SanitizeUserPromptResponse:
    """
    Sanitizes a user prompt using Google Cloud's Model Armor API.

    Args:
        user_prompt (str): The user prompt to be sanitized.

    Returns:
        modelarmor_v1.SanitizeUserPromptResponse: The response from the Model Armor API containing the sanitized prompt.
    """
    print(f"[Callback] Sanitizing user prompt: {user_prompt}")

    try:
        # Initialize request argument(s).
        user_prompt_data = modelarmor_v1.DataItem(text=user_prompt)

        # Prepare request for sanitizing the defined prompt.
        request = modelarmor_v1.SanitizeUserPromptRequest(
            name=f"projects/{globals.project_id}/locations/{globals.location_id}/templates/{globals.template_id}",
            user_prompt_data=user_prompt_data,
        )

        # Sanitize the user prompt.
        response = globals.model_armor_client.sanitize_user_prompt(request=request)

        # Sanitization Result.
        #print(f"[Callback] Sanitization result: {response}")
        return response

    except Exception as e:
        print(f"[Error] Failed to sanitize user prompt: {e}")
        raise

def sanitize_model_response(response_content: str) -> modelarmor_v1.SanitizeModelResponseResponse:
    """
    Sanitizes LLM response content using Google Cloud's Model Armor API.

    Args:
        response_content (str): The LLM response content to be sanitized.

    Returns:
        modelarmor_v1.SanitizeModelResponseResponse: The response from the Model Armor API containing the sanitized content.
    """
    print(f"[Callback] Sanitizing response content: {response_content}")

    try:
        # Initialize request argument(s).
        response_content_data = modelarmor_v1.DataItem(text=response_content)

        # Prepare request for sanitizing the defined response content.
        request = modelarmor_v1.SanitizeModelResponseRequest(
            name=f"projects/{globals.project_id}/locations/{globals.location_id}/templates/{globals.template_id}",
            model_response_data=response_content_data,
        )

        # Sanitize the response content.
        response = globals.model_armor_client.sanitize_model_response(request=request)

        # Sanitization Result.
        #print(f"[Callback] Sanitization result: {response}")
        return response

    except Exception as e:
        print(f"[Error] Failed to sanitize response content: {e}")
        raise