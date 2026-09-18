from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
import logging
import json
import asyncio

from app.api.deps import AgentDep
from app.api.schemas.chat import ChatRequest
from app.core.session_store import get_session_store

router = APIRouter()
logger = logging.getLogger(__name__)


async def sse_generator(agent, query: str, session_id: str, prior_history):
    """
    Consumes the agent's async generator and formats each event as SSE.
    
    SSE Protocol:
      event: <type>\n
      data: <json>\n\n
    """
    final_answer = None
    
    try:
        async for event in agent.run_stream(
            query=query,
            session_id=session_id,
            prior_history=prior_history
        ):
            event_type = event.get("event", "message")
            event_data = event.get("data", {})
            
            # Capture final answer for session storage
            if event_type == "done":
                final_answer = event_data.get("answer")
            
            sse_line = f"event: {event_type}\ndata: {json.dumps(event_data)}\n\n"
            yield sse_line
            
            # Small yield to allow the event loop to flush
            await asyncio.sleep(0)
        
        # Save messages to session store after streaming completes
        if final_answer:
            store = get_session_store()
            store.get_or_create(session_id)
            store.add_messages(session_id, [
                {"role": "user", "content": query},
                {"role": "assistant", "content": final_answer}
            ])
            logger.info(f"Saved conversation to session: {session_id}")
            
    except Exception as e:
        logger.error(f"SSE stream error: {e}")
        error_event = f"event: error\ndata: {json.dumps({'message': str(e)})}\n\n"
        yield error_event


@router.post(
    "/stream",
    summary="Chat with Agent (Streaming SSE)",
    description="Sends a query and streams back SSE events for real-time UI updates.",
)
async def chat_stream(
    request: ChatRequest,
    agent: AgentDep,
):
    """
    Streaming chat endpoint using Server-Sent Events.
    Returns a stream of typed events: plan, status, tool_call, tool_result, token, done.
    """
    try:
        session_id = request.session_id or "default"
        store = get_session_store()
        prior_history = store.get_history(session_id)
        
        return StreamingResponse(
            sse_generator(agent, request.query, session_id, prior_history),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no",  # Disable nginx buffering
            }
        )
    except Exception as e:
        logger.error(f"Stream setup failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
