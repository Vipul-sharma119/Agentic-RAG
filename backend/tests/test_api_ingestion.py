from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock, AsyncMock
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

@patch("app.api.routes.ingestion.IngestionPipeline")
def test_ingest_txt_file(mock_pipeline_cls):
    # Mock pipeline run
    mock_instance = MagicMock()
    mock_instance.run = AsyncMock(return_value=5) # 5 chunks
    mock_pipeline_cls.return_value = mock_instance
    
    # Create a dummy file content
    file_content = b"This is a test document."
    files = {"file": ("test.txt", file_content, "text/plain")}
    
    response = client.post("/api/v1/ingest/", files=files)
    
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "File ingested successfully"
    assert data["chunks_processed"] == 5
    assert data["filename"] == "test.txt"

@patch("app.api.routes.ingestion.IngestionPipeline")
def test_ingest_invalid_file_type(mock_pipeline_cls):
    file_content = b"content"
    files = {"file": ("test.exe", file_content, "application/octet-stream")}
    
    response = client.post("/api/v1/ingest/", files=files)
    
    assert response.status_code == 400
    assert "Unsupported file type" in response.json()["detail"]

def test_ingest_no_file():
    response = client.post("/api/v1/ingest/")
    assert response.status_code == 422 # FastAPI validations for missing field
