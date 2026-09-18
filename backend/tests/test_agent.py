import pytest
from unittest.mock import MagicMock, patch, AsyncMock
from app.agent.agent import Agent

@pytest.mark.asyncio
@patch("app.agent.agent.get_planner")
@patch("app.agent.agent.get_groq_client")
async def test_agent_run(mock_get_client, mock_get_planner):
    # Mock Planner
    mock_planner = MagicMock()
    mock_planner.create_plan = AsyncMock(return_value=["Step 1"])
    mock_get_planner.return_value = mock_planner
    
    # Mock LLM
    mock_llm = MagicMock()
    # Sequence of decisions: 1. Tool Use, 2. Finish
    mock_llm.generate = AsyncMock(side_effect=[
        MagicMock(choices=[MagicMock(message=MagicMock(content='{"type": "tool_use", "tool": "calculator", "args": {"expression": "1+1"}}'))]),
        MagicMock(choices=[MagicMock(message=MagicMock(content='{"type": "finish", "content": "The answer is 2"}'))])
    ])
    mock_get_client.return_value = mock_llm
    
    agent = Agent()
    result = await agent.run("What is 1+1?")
    
    assert result["query"] == "What is 1+1?"
    assert result["answer"] == "The answer is 2"
    assert len(result["history"]) >= 2 # Tool req + Tool result
