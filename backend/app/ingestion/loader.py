import logging
import os
from typing import List, Dict, Any
from pypdf import PdfReader

logger = logging.getLogger(__name__)

class Loader:
    """
    Handles loading of documents from file paths.
    Supports .txt and .pdf files.
    """
    
    @staticmethod
    def load(file_path: str) -> List[Dict[str, Any]]:
        """
        Loads a file and returns a list of documents (dicts with 'content' and 'metadata').
        Each page in a PDF is considered a separate document chunk initially.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
            
        _, ext = os.path.splitext(file_path)
        ext = ext.lower()
        
        if ext == '.pdf':
            return Loader._load_pdf(file_path)
        elif ext == '.txt':
            return Loader._load_txt(file_path)
        else:
            raise ValueError(f"Unsupported file extension: {ext}")

    @staticmethod
    def _load_pdf(file_path: str) -> List[Dict[str, Any]]:
        docs = []
        try:
            reader = PdfReader(file_path)
            for i, page in enumerate(reader.pages):
                text = page.extract_text()
                if text:
                    docs.append({
                        "content": text,
                        "metadata": {
                            "source": file_path,
                            "page": i + 1,
                            "type": "pdf"
                        }
                    })
            logger.info(f"Loaded {len(docs)} pages from PDF: {file_path}")
            return docs
        except Exception as e:
            logger.error(f"Failed to load PDF {file_path}: {e}")
            raise e

    @staticmethod
    def _load_txt(file_path: str) -> List[Dict[str, Any]]:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            
            logger.info(f"Loaded text file: {file_path}")
            return [{
                "content": text,
                "metadata": {
                    "source": file_path,
                    "type": "txt"
                }
            }]
        except Exception as e:
            logger.error(f"Failed to load text file {file_path}: {e}")
            raise e
