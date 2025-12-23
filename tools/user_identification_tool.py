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

def get_account_information(ph_no, zipcode)-> dict:
    """
    Retrieves mock account information for a customer based on phone number and zipcode.
    Args:
        ph_no (str): The customer's phone number.
        zipcode (str): The customer's zipcode.
    Returns:
        Dict: A JSON dict containing the account information, including customer ID, account ID, customer type, account status, name, date of birth, address, and phone number.
    """
    print(f"Fetching account information for Phone No: {ph_no}, Zipcode: {zipcode}")
    # Mock response data
    response_data = {
        "customer_id": "venky-123",
        "account_id": "987654321",
        "customer_type": "Individual",
        "account_status": "Active",
        "customer_name": "venky muthu",
        "customer_dob": "1990-01-01",
        "customer_address": f"123 Main St Mississauga {zipcode} ON",
        "customer_ph_no": ph_no
    }
    
    # Create a JSON response
    response = {
        "status": "success",
        "data": response_data
    }
    
    return response

def exit_agent():
    """
    Call this function ONLY when phone number or zipcode is invalid and the user has been informed about failed authentication.
    """
    print("🚪 Exiting from the agent reasoning...")
    return {"status": "unauthenticated", "message": "Authenitcation failed."}