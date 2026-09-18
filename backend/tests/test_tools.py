import pytest
from unittest.mock import MagicMock, patch
from app.agent.tools import RetrievalTool, CalculatorTool

@patch("app.agent.tools.get_retriever")
@patch("app.agent.tools.get_reranker")
def test_retrieval_tool(mock_get_reranker, mock_get_retriever):
    # Setup Mocks
    mock_retriever = MagicMock()
    mock_retriever.retrieve.return_value = [{"content": "doc1"}]
    mock_get_retriever.return_value = mock_retriever
    
    mock_reranker = MagicMock()
    mock_reranker.rerank.return_value = [{"content": "doc1", "rerank_score": 0.9}]
    mock_get_reranker.return_value = mock_reranker
    
    tool = RetrievalTool()
    result = tool.run("query")
    
    assert "Document 1" in result
    assert "Score: 0.90" in result
    assert "doc1" in result

def test_calculator_tool():
    tool = CalculatorTool()
    assert tool.run("1 + 1") == "2"
    assert tool.run("2 * 3") == "6"
    assert "Invalid" in tool.run("import os")
