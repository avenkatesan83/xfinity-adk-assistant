import uuid
import globals
from fastapi import HTTPException
from google.genai.types import Content, Part
from api.helper.agent_helper import llm_response_to_text

async def create_new_user_session() -> str:
    """
    Creates a new user session id
    """
    try:
        print("\n🚀 Creating a new user session")        
        # Create a new user session
        """sId = globals.user_id + "-" + str(uuid.uuid4())
        print(f"Newly created User Session ID: {sId}")
        session = await globals.session_service.create_session(app_name=globals.app_name,
                        user_id=globals.user_id,
                        session_id=sId)"""
        session = await globals.session_service.create_session(app_name=globals.app_name,
                        user_id=globals.user_id)
        print(f"Initial state of session : {session.state}")
        return session.id
    
    except Exception as e:
        print(f"Agent Execution Error: {e}")
        raise HTTPException(
            status_code=500, detail=f"Error creating new user session request with agent: {e}"
        )

async def handle_user_query(session_id: str, user_prompt: str) -> str:
    """
    Handles a user query request
    """
    try:
        print("\n🚀 Handling user prompt with ADK Agent..."
              f"\nPrompt: {user_prompt}")
        
        # The global_runner type hint ensures correct methods are used
        #runner: InMemoryRunner = globals.global_runner 
        #response_text = await runner.run_debug(request.user_prompt)
        if user_prompt and user_prompt == globals.welcome_event:
            user_prompt = globals.default_user_prompt
            
        print(f"User Session ID: {session_id}")
        user_message = Content(parts=[Part(text=user_prompt)])
        # LLM Streaming...
        llmResponse = globals.global_runner.run_async(user_id=globals.user_id, 
                                               session_id=session_id, 
                                               new_message=user_message)
        return await llm_response_to_text(llmResponse)

    except Exception as e:
        print(f"Agent Execution Error: {e}")
        raise HTTPException(
            status_code=500, detail=f"Error handling user prompt with agent: {e}"
        )