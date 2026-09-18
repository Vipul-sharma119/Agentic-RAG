import pytest
from unittest.mock import MagicMock, patch
from app.retrieval.embedder import Embedder

@patch("app.retrieval.embedder.InferenceClient")
@patch("app.retrieval.embedder.settings")
def test_embedder_initialization(mock_settings, mock_inference_client):
    mock_settings.EMBEDDING_MODEL = "BAAI/bge-m3"
    mock_settings.HF_TOKEN = "dummy_token"
    
    embedder = Embedder()
    
    mock_inference_client.assert_called_with(
        provider="hf-inference",
        api_key="dummy_token",
        model="BAAI/bge-m3"
    )
    assert embedder.client is not None

@patch("app.retrieval.embedder.InferenceClient")
@patch("app.retrieval.embedder.settings")
def test_embed_text(mock_settings, mock_inference_client):
    mock_settings.HF_TOKEN = "dummy"
    mock_client_instance = MagicMock()
    mock_inference_client.return_value = mock_client_instance
    
    # Mock feature_extraction return (simple list)
    mock_client_instance.feature_extraction.return_value = [0.1, 0.2, 0.3]
    
    embedder = Embedder()
    result = embedder.embed_text("test")
    
    assert result == [0.1, 0.2, 0.3]
    mock_client_instance.feature_extraction.assert_called_with("test")

@patch("app.retrieval.embedder.InferenceClient")
@patch("app.retrieval.embedder.settings")
def test_embed_text_numpy(mock_settings, mock_inference_client):
    mock_settings.HF_TOKEN = "dummy"
    mock_client_instance = MagicMock()
    mock_inference_client.return_value = mock_client_instance
    
    # Mock numpy-like return
    mock_numpy = MagicMock()
    mock_numpy.tolist.return_value = [0.1, 0.2, 0.3]
    mock_client_instance.feature_extraction.return_value = mock_numpy
    
    embedder = Embedder()
    result = embedder.embed_text("test")
    
    assert result == [0.1, 0.2, 0.3]
