from typing import Optional, Any
from pydantic import BaseModel, Field

class ErrorResponse(BaseModel):
    detail: str = Field(..., description="Error description.")
    code: Optional[str] = Field(None, description="Error code.")

class HealthResponse(BaseModel):
    status: str = Field(..., description="Health status (e.g., 'ok').")
    app_name: str = Field(..., description="Application name.")
    version: str = Field(..., description="Application version.")
