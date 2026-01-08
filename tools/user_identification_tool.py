import globals
import re

def get_user_data_from_memory() -> dict:
    """
    Retrieves the user data stored in globals.

    Returns:
        dict: The user data dictionary.
    """
    print("globals user data:", globals.user_data)

    results = parse_memories_to_dict(globals.user_data)
    print("results:", results) 
    
    return results

def get_memory_text_parts(memories):
    """
    Extracts all text values from a SearchMemoryResponse or list of MemoryEntry objects.
    """
    # 1. Handle the SearchMemoryResponse object seen in your logs
    if hasattr(memories, 'memories'):
        memories = memories.memories
    
    # 2. Safety check: ensure we now have a list to iterate over
    if not isinstance(memories, list):
        print(f"Warning: Expected list after extraction but got {type(memories)}")
        return []

    results = []
    for entry in memories:
        try:
            # The structure is MemoryEntry -> content -> parts -> [Part(text=...)]
            if hasattr(entry, 'content') and hasattr(entry.content, 'parts'):
                for part in entry.content.parts:
                    if hasattr(part, 'text') and part.text:
                        results.append(part.text)
        except Exception as e:
            print(f"Error parsing entry: {e}")
            continue
            
    return results

def parse_memories_to_dict(memories):
    text_list = get_memory_text_parts(memories)
    combined_text = " ".join(text_list)
    
    extracted = {
        "phone_number": re.search(r'(\d{10})', combined_text),
        "zip_code": re.search(r'([A-Z]\d[A-Z]\s?\d[A-Z]\d)', combined_text)
    }

    print("Extracted from memory:", extracted)
    
    return {k: v.group(0) if v else None for k, v in extracted.items()}
# Result: {'phone_number': '4378309822', 'zip_code': 'L5A 0B1'}

def validate_ph_no(ph_no: str) -> str:
    """
    Checks if the provided phone number matches the expected value.

    Args:
        ph_no (str): The phone number to validate.

    Returns:
        str: A JSON-formatted string containing the 'status' set to 'valid' and the phone number in 'data' if valid,
              otherwise 'status' is 'invalid' and 'data' is empty.
    """
    """Validates the phone no."""
    print(f"Validating phone number: {ph_no}")
    response = {"status": "invalid", "data": {}}
    if ph_no == "4378309822":
        response = {"status": "valid", "data": {"ph_no": ph_no}}
        return response
    else:
        return response

def validate_zip_code(zip_code: str) -> str:
    """
    Checks if the provided zip code matches the expected value "L5A0B1".

    Args:
        zip_code (str): The zip code to validate.

    Returns:
        str: A JSON-formatted string containing the 'status' set to 'valid' and the phone number in 'data' if valid,
              otherwise 'status' is 'invalid' and 'data' is empty.
    """
    """Validates the zipcode."""
    print(f"Validating zip code: {zip_code}")
    response = {"status": "invalid", "data": {}}
    if zip_code == "L5A0B1":
        response = {"status": "valid", "data": {"ph_no": zip_code}}
        return response
    else:
        return response

def exit_agent():
    """
    Call this function ONLY when phone number or zipcode is invalid and the user has been informed about failed authentication.
    """
    print("🚪 Exiting from the agent reasoning...")
    return {"status": "unauthenticated", "message": "Authenitcation failed."}