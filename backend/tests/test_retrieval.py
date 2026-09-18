import pytest
from unittest.mock import MagicMock, patch
from app.retrieval.retriever import Retriever

@patch("app.retrieval.retriever.get_embedder")
@patch("app.retrieval.retriever.get_qdrant_client")
def test_retrieve(mock_get_qdrant, mock_get_embedder):
    # Setup mocks
    mock_embedder = MagicMock()
    mock_embedder.embed_text.return_value = [0.1] * 1024 # Mock 1024d vector
    mock_get_embedder.return_value = mock_embedder

    mock_qdrant_wrapper = MagicMock()
    mock_qdrant_wrapper.collection_name = "test_collection"
    mock_client = MagicMock()
    mock_qdrant_wrapper.client = mock_client
    mock_get_qdrant.return_value = mock_qdrant_wrapper

    # Mock search result
    mock_point = MagicMock()
    mock_point.id = "1"
    mock_point.score = 0.9
    mock_point.payload = {"content": "test content", "metadata": {"source": "doc1"}}
    mock_client.search.return_value = [mock_point]

    # Test
    retriever = Retriever()
    results = retriever.retrieve("test query")

    assert len(results) == 1
    assert results[0]["content"] == "test content"
    assert results[0]["score"] == 0.9
    
    # Verify calls
    mock_embedder.embed_text.assert_called_with("test query")
    mock_client.search.assert_called_once() 
    
    # Verify arguments passed to search
    assert mock_client.search.call_args[1]["collection_name"] == "test_collection"
    assert len(mock_client.search.call_args[1]["query_vector"]) == 1024
