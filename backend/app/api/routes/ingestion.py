from fastapi import APIRouter, HTTPException, BackgroundTasks, UploadFile, File, Depends
from typing import List, Any
import shutil
import os
import tempfile
import logging

from app.api.deps import IngestionDep
from app.api.schemas.ingestion import IngestionResponse, IngestionStatus
from app.api.schemas.common import ErrorResponse

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post(
    "/",
    response_model=IngestionResponse,
    status_code=202,
    summary="Ingest Document",
    description="Uploads and processes a document (PDF/TXT) for RAG.",
    responses={
        400: {"model": ErrorResponse, "description": "Invalid file type or missing file."},
        500: {"model": ErrorResponse, "description": "Internal server error during processing."}
    }
)
async def ingest_file(
    pipeline: IngestionDep,
    file: UploadFile = File(...),
):
    """
    Ingests a file into the vector database.
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded")
    
    filename = file.filename.lower()
    if not (filename.endswith(".pdf") or filename.endswith(".txt")):
        raise HTTPException(status_code=400, detail="Unsupported file type. Only .pdf and .txt are supported.")

    # Save file temporarily
    tmp_path = ""
    try:
        suffix = ".pdf" if filename.endswith(".pdf") else ".txt"
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
            shutil.copyfileobj(file.file, tmp_file)
            tmp_path = tmp_file.name
            
        logger.info(f"File uploaded to temporary path: {tmp_path}")
        
    except Exception as e:
        logger.error(f"Failed to save uploaded file: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")

    try:
        # Run pipeline synchronously for MVP feedback loop
        # In production, this should ideally be a BackgroundTask if extensive
        chunks_count = await pipeline.run([tmp_path])
        
        # Cleanup
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        
        return IngestionResponse(
            message="File ingested successfully",
            filename=file.filename,
            chunks_processed=chunks_count
        )
        
    except Exception as e:
        logger.error(f"Ingestion failed: {e}")
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {str(e)}")
