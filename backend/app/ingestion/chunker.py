from typing import List, Dict, Any
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.core.settings import settings

class Chunker:
    """
    Handles splitting of text into chunks.
    """
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        # Default settings if not provided? 
        # Ideally should come from settings, but for now we default here or pass in.
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            is_separator_regex=False,
        )

    def chunk(self, docs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Splits documents into smaller chunks.
        Preserves metadata.
        """
        chunked_docs = []
        for doc in docs:
            content = doc.get("content", "")
            metadata = doc.get("metadata", {})
            
            chunks = self.text_splitter.split_text(content)
            
            for i, chunk_text in enumerate(chunks):
                chunk_metadata = metadata.copy()
                chunk_metadata["chunk_index"] = i
                
                chunked_docs.append({
                    "content": chunk_text,
                    "metadata": chunk_metadata
                })
                
        return chunked_docs
