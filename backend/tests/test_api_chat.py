from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock, MagicMock
from app.main import app

client = TestClient(app)

@patch("app.api.routes.chat.get_agent")
def test_chat_endpoint(mock_get_agent):
    # Mock Agent
    mock_agent = MagicMock()
    mock_run = AsyncMock(return_value={
        "query": "hello",
        "answer": "world",
        "history": [{"role": "user", "content": "hello"}]
    })
    mock_agent.run = mock_run
    mock_get_agent.return_value = mock_agent
    
    response = client.post("/api/v1/chat/", json={"query": "hello"})
    
    assert response.status_code == 200
    data = response.json()
    assert data["answer"] == "world"
    assert len(data["history"]) == 1

@patch("app.api.routes.chat.get_agent")
def test_chat_error(mock_get_agent):
    mock_agent = MagicMock()
    mock_agent.run = AsyncMock(side_effect=Exception("Agent error"))
    mock_get_agent.return_value = mock_agent
    
    response = client.post("/api/v1/chat/", json={"query": "hello"})
    
    assert response.status_code == 500
