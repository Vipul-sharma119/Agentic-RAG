from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
import logging

from app.core.session_store import get_session_store

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get(
    "/",
    summary="List Sessions",
    description="Returns a list of all conversation sessions.",
)
async def list_sessions() -> List[Dict[str, Any]]:
    store = get_session_store()
    return store.list_sessions()


@router.get(
    "/{session_id}",
    summary="Get Session",
    description="Returns the full conversation history for a session.",
)
async def get_session(session_id: str) -> Dict[str, Any]:
    store = get_session_store()
    session = store.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail=f"Session '{session_id}' not found.")
    return session


@router.delete(
    "/{session_id}",
    summary="Delete Session",
    description="Deletes a conversation session.",
)
async def delete_session(session_id: str) -> Dict[str, str]:
    store = get_session_store()
    deleted = store.delete_session(session_id)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Session '{session_id}' not found.")
    return {"message": f"Session '{session_id}' deleted."}
