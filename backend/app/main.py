from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import logging
import uvicorn

from app.core.settings import settings
from app.api.routes import ingestion, chat, sessions, stream, ingest_stream
from app.api.schemas.common import HealthResponse

# Configure logging
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting up Agentic RAG System...")
    yield
    # Shutdown
    logger.info("Shutting down Agentic RAG System...")

app = FastAPI(
    title=settings.APP_NAME,
    description="Production-grade Agentic RAG API with Autonomous Planning.",
    version="0.1.0",
    docs_url="/docs" if settings.APP_ENV == "development" else None,
    redoc_url="/redoc" if settings.APP_ENV == "development" else None,
    openapi_url="/openapi.json",
    lifespan=lifespan
)

# CORS Configuration
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global Exception Handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error", "code": "INTERNAL_ERROR"},
    )

# Include Routers
app.include_router(ingestion.router, prefix=f"{settings.API_V1_STR}/ingest", tags=["Ingestion"])
app.include_router(chat.router, prefix=f"{settings.API_V1_STR}/chat", tags=["Chat"])
app.include_router(stream.router, prefix=f"{settings.API_V1_STR}/chat", tags=["Chat Streaming"])
app.include_router(sessions.router, prefix=f"{settings.API_V1_STR}/sessions", tags=["Sessions"])
app.include_router(ingest_stream.router, prefix=f"{settings.API_V1_STR}/ingest", tags=["Ingestion Streaming"])

@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    return HealthResponse(
        status="ok",
        app_name=settings.APP_NAME,
        version="0.1.0"
    )

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
