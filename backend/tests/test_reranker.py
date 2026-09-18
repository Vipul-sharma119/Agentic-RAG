import pytest
from unittest.mock import MagicMock, patch
from app.retrieval.reranker import Reranker

@patch("app.retrieval.reranker.CrossEncoder")
def test_rerank(mock_cross_encoder):
    # Setup mock
    mock_model = MagicMock()
    # Mock scores for 3 docs
    mock_model.predict.return_value = [0.1, 0.9, 0.5]
    mock_cross_encoder.return_value = mock_model
    
    reranker = Reranker()
    
    docs = [
        {"content": "low relevance", "id": 1},
        {"content": "high relevance", "id": 2},
        {"content": "medium relevance", "id": 3}
    ]
    
    reranked = reranker.rerank("query", docs, top_k=3)
    
    assert len(reranked) == 3
    assert reranked[0]["id"] == 2 # Score 0.9
    assert reranked[1]["id"] == 3 # Score 0.5
    assert reranked[2]["id"] == 1 # Score 0.1
    assert reranked[0]["rerank_score"] == 0.9

@patch("app.retrieval.reranker.CrossEncoder")
def test_rerank_empty(mock_cross_encoder):
    mock_cross_encoder.return_value = MagicMock()
    reranker = Reranker()
    assert reranker.rerank("query", []) == []
