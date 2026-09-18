import pytest
from unittest.mock import MagicMock, patch, mock_open
from app.ingestion.loader import Loader
from app.ingestion.cleaner import Cleaner
from app.ingestion.chunker import Chunker
from app.ingestion.pipeline import IngestionPipeline

# Loader Tests
def test_loader_txt():
    with patch("builtins.open", mock_open(read_data="test content")):
        docs = Loader._load_txt("test.txt")
        assert len(docs) == 1
        assert docs[0]["content"] == "test content"
        assert docs[0]["metadata"]["type"] == "txt"

@patch("app.ingestion.loader.PdfReader")
def test_loader_pdf(mock_pdf_reader):
    mock_page = MagicMock()
    mock_page.extract_text.return_value = "pdf page content"
    mock_pdf_reader.return_value.pages = [mock_page]
    
    docs = Loader._load_pdf("test.pdf")
    assert len(docs) == 1
    assert docs[0]["content"] == "pdf page content"
    assert docs[0]["metadata"]["type"] == "pdf"

# Cleaner Tests
def test_cleaner():
    raw_docs = [{"content": "  hello   world  \n\n\n  ", "metadata": {}}]
    cleaned = Cleaner.clean(raw_docs)
    assert cleaned[0]["content"] == "hello world"

# Chunker Tests
def test_chunker():
    chunker = Chunker(chunk_size=10, chunk_overlap=0)
    docs = [{"content": "helloworld12345", "metadata": {"source": "test"}}]
    # "helloworld" (10 chars), "12345" (5 chars)
    # Recursively splits. 
    
    chunks = chunker.chunk(docs)
    assert len(chunks) >= 2
    assert chunks[0]["metadata"]["source"] == "test"
    assert "chunk_index" in chunks[0]["metadata"]

# Pipeline Tests
@pytest.mark.asyncio
@patch("app.ingestion.pipeline.Loader")
@patch("app.ingestion.pipeline.Cleaner")
@patch("app.ingestion.pipeline.Chunker")
@patch("app.ingestion.pipeline.get_embedder")
@patch("app.ingestion.pipeline.get_qdrant_client")
async def test_pipeline_run(mock_get_qdrant, mock_get_embedder, mock_chunker_cls, mock_cleaner, mock_loader):
    # Setup mocks
    mock_pipeline_chunker = MagicMock()
    mock_chunker_cls.return_value = mock_pipeline_chunker
    
    mock_embedder = MagicMock()
    mock_get_embedder.return_value = mock_embedder
    
    mock_qdrant = MagicMock()
    mock_get_qdrant.return_value = mock_qdrant
    
    # Mock data flow
    mock_loader.load.return_value = [{"content": "raw", "metadata": {}}]
    mock_cleaner.clean.return_value = [{"content": "cleaned", "metadata": {}}]
    mock_pipeline_chunker.chunk.return_value = [{"content": "chunk", "metadata": {}}]
    mock_embedder.embed_text.return_value = [0.1, 0.2]
    
    pipeline = IngestionPipeline()
    count = await pipeline.run(["test.txt"])
    
    assert count == 1
    mock_loader.load.assert_called_with("test.txt")
    mock_cleaner.clean.assert_called()
    mock_pipeline_chunker.chunk.assert_called()
    mock_embedder.embed_text.assert_called_with("chunk")
    mock_qdrant.upsert.assert_called_once()
