from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import StreamingResponse
import shutil
import os
import tempfile
import logging
import json
import asyncio

from app.api.deps import IngestionDep

router = APIRouter()
logger = logging.getLogger(__name__)


async def ingest_sse_generator(pipeline, file_path: str, original_filename: str):
    """
    Consumes the pipeline's async generator and formats as SSE.
    """
    try:
        # Initial event
        yield f"event: status\ndata: {json.dumps({'step': 'started', 'message': f'Processing {original_filename}...'})}\n\n"
        
        async for event in pipeline.run_stream(file_path):
            event_type = event.get("event", "status")
            event_data = event.get("data", {})
            
            yield f"event: {event_type}\ndata: {json.dumps(event_data)}\n\n"
            await asyncio.sleep(0)
        
    except Exception as e:
        logger.error(f"Ingest SSE error: {e}")
        yield f"event: error\ndata: {json.dumps({'message': str(e)})}\n\n"
    
    finally:
        # Cleanup temp file
        if os.path.exists(file_path):
            os.remove(file_path)


@router.post(
    "/stream",
    summary="Ingest Document (Streaming SSE)",
    description="Uploads and processes a document with real-time progress via SSE.",
)
async def ingest_file_stream(
    pipeline: IngestionDep,
    file: UploadFile = File(...),
):
    """
    Streaming ingestion endpoint — returns SSE events for each pipeline stage.
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded")
    
    filename = file.filename.lower()
    if not (filename.endswith(".pdf") or filename.endswith(".txt")):
        raise HTTPException(status_code=400, detail="Unsupported file type. Only .pdf and .txt.")
    
    # Save file temporarily
    try:
        suffix = ".pdf" if filename.endswith(".pdf") else ".txt"
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
            shutil.copyfileobj(file.file, tmp_file)
            tmp_path = tmp_file.name
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")
    
    return StreamingResponse(
        ingest_sse_generator(pipeline, tmp_path, file.filename),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        }
    )
