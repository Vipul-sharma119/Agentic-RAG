import pytest
from unittest.mock import MagicMock, patch
from app.llm.groq_client import GroqClient
from groq import GroqError

# Mock settings to avoid needing .env file
@pytest.fixture
def mock_settings(monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "test_key")
    monkeypatch.setattr("app.core.settings.settings.GROQ_API_KEY", "test_key")

def test_groq_client_initialization(mock_settings):
    client = GroqClient()
    assert client.api_key == "test_key"

@patch("app.llm.groq_client.Groq")
def test_chat_completion_success(mock_groq, mock_settings):
    # Setup mock
    mock_client_instance = MagicMock()
    mock_groq.return_value = mock_client_instance
    
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(content="Hello world"))]
    mock_client_instance.chat.completions.create.return_value = mock_response

    client = GroqClient()
    messages = [{"role": "user", "content": "Hi"}]
    response = client.chat_completion(messages)

    assert response == mock_response
    mock_client_instance.chat.completions.create.assert_called_once()
    
    # Check arguments
    call_kwargs = mock_client_instance.chat.completions.create.call_args[1]
    assert call_kwargs["messages"] == messages
    assert call_kwargs["model"] == "llama3-70b-8192" # Default in settings is this, or we can mock it.

@patch("app.llm.groq_client.Groq")
def test_chat_completion_failure(mock_groq, mock_settings):
    mock_client_instance = MagicMock()
    mock_groq.return_value = mock_client_instance
    
    # Simulate API error
    mock_client_instance.chat.completions.create.side_effect = GroqError("API Error", MagicMock(status_code=400), {})

    client = GroqClient()
    messages = [{"role": "user", "content": "Hi"}]

    with pytest.raises(GroqError):
        client.chat_completion(messages)
