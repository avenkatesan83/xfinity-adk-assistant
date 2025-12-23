import globals
import time
import uuid
from fastapi import APIRouter, HTTPException
from agents.root.customer_support_agent import Runner, InMemoryRunner
from google.genai.types import Content, Part
from api.schema.agent_schema import QueryRequest, QueryResponse
from api.schema.session_schema import SessionResponse
from api.controller.agent_controller import process_new_session, process_user_query

# Initialize the APIRouter
agent_router = APIRouter(
    prefix="/adk-agent-fastapi",
    tags=["ADK Agent Fastapi"]
)

@agent_router.post("/newusersession", response_model=SessionResponse)
async def create_session():
    """
    Receives a request to create a new user session id
    Endpoint: /root-agent/newusersession
    """

    try:
        print("\n🚀 Rotuing a request for new user session")        
        # Create a new user session
        sId = await process_new_session()
        return SessionResponse(session_id=sId)
    
    except Exception as e:
        print(f"Agent Execution Error: {e}")
        raise HTTPException(
            status_code=500, detail=f"Error routing new user session request with agent: {e}"
        )

@agent_router.post("/query", response_model=QueryResponse)
async def handle_query(request: QueryRequest):
    """
    Receives a user prompt and passes it to the ADK Agent for processing.
    Endpoint: /root-agent/query
    """
    if not globals.global_runner:
        raise HTTPException(
            status_code=503, detail="Agent service is not initialized."
        )
    
    try:
        print("\n🚀 Rotuing a request to ADK agent for handling user query")        
        # Handle the user query
        agentResponse = await process_user_query(request.session_id, request.prompt)
        return QueryResponse(response=agentResponse)
    
    except Exception as e:
        print(f"Agent Execution Error: {e}")
        raise HTTPException(
            status_code=500, detail=f"Error routing user query request with agent: {e}"
        )