from typing import Generator, Annotated
from fastapi import Depends
from app.core.settings import settings, Settings
from app.agent.agent import get_agent, Agent
from app.ingestion.pipeline import IngestionPipeline

# Settings Dependency
def get_settings() -> Settings:
    return settings

# Agent Dependency
def get_agent_service() -> Agent:
    """
    Dependency to get the Agent instance.
    In a real app, this might pull from a pool or context vars.
    Currently, get_agent() returns a fresh instance or cached one.
    """
    return get_agent()

# Ingestion Pipeline Dependency
def get_ingestion_pipeline() -> IngestionPipeline:
    """
    Dependency to get the IngestionPipeline instance.
    """
    return IngestionPipeline()

# Type Aliases for clearer route signatures
SettingsDep = Annotated[Settings, Depends(get_settings)]
AgentDep = Annotated[Agent, Depends(get_agent_service)]
IngestionDep = Annotated[IngestionPipeline, Depends(get_ingestion_pipeline)]
