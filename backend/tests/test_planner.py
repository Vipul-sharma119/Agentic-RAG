import pytest
from unittest.mock import MagicMock, patch, AsyncMock
from app.agent.planner import Planner
from app.agent.state import AgentState

@pytest.mark.asyncio
@patch("app.agent.planner.get_groq_client")
async def test_create_plan(mock_get_client):
    # Mock LLM response
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(content='{"steps": ["Step 1", "Step 2"]}'))]
    mock_client.generate = AsyncMock(return_value=mock_response)
    mock_get_client.return_value = mock_client
    
    planner = Planner()
    state = AgentState(query="Test query")
    
    plan = await planner.create_plan(state)
    
    assert len(plan) == 2
    assert plan[0] == "Step 1"
    assert plan[1] == "Step 2"

@pytest.mark.asyncio
@patch("app.agent.planner.get_groq_client")
async def test_create_plan_failure(mock_get_client):
    # Mock failure
    mock_client = MagicMock()
    mock_client.generate = AsyncMock(side_effect=Exception("LLM error"))
    mock_get_client.return_value = mock_client
    
    planner = Planner()
    state = AgentState(query="Test query")
    
    # Should return fallback plan
    plan = await planner.create_plan(state)
    
    assert len(plan) > 0
    assert "Retrieve relevant information" in plan
