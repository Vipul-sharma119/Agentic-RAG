import pytest
from unittest.mock import MagicMock, patch
from qdrant_client.http import models
from app.retrieval.qdrant_client import QdrantClientWrapper

@patch("app.retrieval.qdrant_client.QdrantClientLib")
@patch("app.retrieval.qdrant_client.settings")
def test_initialization_collection_exists(mock_settings, mock_qdrant_lib):
    # Setup settings
    mock_settings.QDRANT_HOST = "localhost"
    mock_settings.QDRANT_PORT = 6333
    mock_settings.QDRANT_API_KEY = None
    mock_settings.QDRANT_COLLECTION_NAME = "test_collection"
    mock_settings.EMBEDDING_DIM = 1024

    # Setup Qdrant Client Mock
    mock_client_instance = MagicMock()
    mock_qdrant_lib.return_value = mock_client_instance
    
    # Simulate collection exists (no exception raised)
    mock_client_instance.get_collection.return_value = MagicMock()

    wrapper = QdrantClientWrapper()
    
    # Assertions
    mock_client_instance.get_collection.assert_called_with("test_collection")
    mock_client_instance.create_collection.assert_not_called()

@patch("app.retrieval.qdrant_client.QdrantClientLib")
@patch("app.retrieval.qdrant_client.settings")
def test_initialization_collection_create(mock_settings, mock_qdrant_lib):
    # Setup settings
    mock_settings.QDRANT_HOST = "localhost"
    mock_settings.QDRANT_PORT = 6333
    mock_settings.QDRANT_API_KEY = None
    mock_settings.QDRANT_COLLECTION_NAME = "test_collection"
    mock_settings.EMBEDDING_DIM = 1024

    # Setup Qdrant Client Mock
    mock_client_instance = MagicMock()
    mock_qdrant_lib.return_value = mock_client_instance
    
    # Simulate collection NOT found (raises ValueError or UnexpectedResponse)
    mock_client_instance.get_collection.side_effect = ValueError("Not found")

    wrapper = QdrantClientWrapper()
    
    # Assertions
    mock_client_instance.get_collection.assert_called_with("test_collection")
    mock_client_instance.create_collection.assert_called_once()
    call_args = mock_client_instance.create_collection.call_args
    assert call_args[1]['collection_name'] == "test_collection"
    assert call_args[1]['vectors_config'].size == 1024

@patch("app.retrieval.qdrant_client.QdrantClientLib")
def test_upsert(mock_qdrant_lib):
    mock_client_instance = MagicMock()
    mock_qdrant_lib.return_value = mock_client_instance
    
    wrapper = QdrantClientWrapper()
    
    points = [models.PointStruct(id=1, vector=[0.1]*1024, payload={})]
    wrapper.upsert(points)
    
    mock_client_instance.upsert.assert_called_once()

@patch("app.retrieval.qdrant_client.QdrantClientLib")
def test_search(mock_qdrant_lib):
    mock_client_instance = MagicMock()
    mock_qdrant_lib.return_value = mock_client_instance
    
    wrapper = QdrantClientWrapper()
    
    wrapper.search(query_vector=[0.1]*1024)
    
    mock_client_instance.search.assert_called_once()
