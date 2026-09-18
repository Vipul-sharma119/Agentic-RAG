from typing import Optional
from pydantic import BaseModel, Field

class IngestionResponse(BaseModel):
    message: str = Field(..., description="Status message.")
    filename: str = Field(..., description="Name of the ingested file.")
    chunks_processed: int = Field(..., description="Number of chunks created and stored.")

class IngestionStatus(BaseModel):
    status: str = Field(..., description="Current status of the ingestion job.")
    details: Optional[str] = Field(None, description="Additional details or error message.")
