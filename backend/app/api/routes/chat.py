from fastapi import APIRouter, HTTPException
import logging

from app.api.deps import AgentDep
from app.api.schemas.chat import ChatRequest, ChatResponse
from app.api.schemas.common import ErrorResponse
from app.core.session_store import get_session_store

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post(
    "/",
    response_model=ChatResponse,
    summary="Chat with Agent",
    description="Sends a query to the autonomous agent which plans and executes steps to answer.",
    responses={
        500: {"model": ErrorResponse, "description": "Agent execution failed."}
    }
)
async def chat(
    request: ChatRequest,
    agent: AgentDep
):
    """
    Chat endpoint with session persistence.
    """
    try:
        session_id = request.session_id or "default"
        store = get_session_store()
        
        # Load prior history for context
        prior_history = store.get_history(session_id)
        
        # Run agent with session context
        result = await agent.run(
            query=request.query,
            session_id=session_id,
            prior_history=prior_history
        )
        
        # Save user message + assistant answer to session
        new_messages = [{"role": "user", "content": request.query}]
        if result.get("answer"):
            new_messages.append({"role": "assistant", "content": result["answer"]})
        
        store.get_or_create(session_id)
        store.add_messages(session_id, new_messages)
        
        return ChatResponse(
            query=result["query"],
            answer=result["answer"],
            plan=result.get("plan", []),
            history=result["history"]
        )
    except Exception as e:
        logger.error(f"Chat failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
