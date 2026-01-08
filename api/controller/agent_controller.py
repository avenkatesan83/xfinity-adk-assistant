
from fastapi import HTTPException
from api.service.agent_service import create_new_user_session, handle_user_query

async def process_new_session(user_id: str) -> str:
    """
    Processes a new user session request
    """
    try:
        print("\n🚀 Processing a request for new user session")        
        # Create a new user session
        return await create_new_user_session(user_id)
    
    except Exception as e:
        print(f"Agent Execution Error: {e}")
        raise HTTPException(
            status_code=500, detail=f"Error processing new user session request with agent: {e}"
        )
    
async def process_user_query(session_id: str, user_id: str, prompt: str) -> str:
    """
    Processes a user query request
    """
    try:
        print("\n🚀 Processing a request for user query")        
        # Create a new user session
        return await handle_user_query(session_id, user_id, prompt)
    
    except Exception as e:
        print(f"Agent Execution Error: {e}")
        raise HTTPException(
            status_code=500, detail=f"Error processing user query request with agent: {e}"
        )