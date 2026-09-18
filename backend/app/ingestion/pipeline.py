import logging
import uuid
import time
import json
from typing import List, Dict, Any, AsyncGenerator
from app.ingestion.loader import Loader
from app.ingestion.cleaner import Cleaner
from app.ingestion.chunker import Chunker
from app.retrieval.embedder import get_embedder
from app.retrieval.qdrant_client import get_qdrant_client
from qdrant_client.http import models

logger = logging.getLogger(__name__)

class IngestionPipeline:
    """
    Orchestrates the document ingestion process.
    """
    
    def __init__(self):
        self.chunker = Chunker()
        self.embedder = get_embedder()
        self.qdrant_client = get_qdrant_client()

    async def run(self, file_paths: List[str]):
        """
        Runs the ingestion pipeline for a list of files (non-streaming).
        """
        total_chunks = 0
        for file_path in file_paths:
            try:
                logger.info(f"Processing file: {file_path}")
                
                docs = Loader.load(file_path)
                logger.debug(f"Loaded {len(docs)} documents/pages")
                
                cleaned_docs = Cleaner.clean(docs)
                logger.debug(f"Cleaned {len(cleaned_docs)} documents")
                
                chunks = self.chunker.chunk(cleaned_docs)
                logger.debug(f"Generated {len(chunks)} chunks")
                
                if not chunks:
                    logger.warning(f"No chunks generated for {file_path}")
                    continue
                
                points = []
                for chunk in chunks:
                    text = chunk["content"]
                    metadata = chunk["metadata"]
                    
                    vector = self.embedder.embed_text(text)
                    point_id = str(uuid.uuid4())
                    payload = {
                        "content": text,
                        "metadata": metadata
                    }
                    
                    points.append(models.PointStruct(
                        id=point_id,
                        vector=vector,
                        payload=payload
                    ))
                
                self.qdrant_client.upsert(points)
                total_chunks += len(points)
                logger.info(f"Successfully ingested {len(points)} chunks from {file_path}")
                
            except Exception as e:
                import traceback
                traceback.print_exc()
                logger.error(f"Failed to ingest file {file_path}: {e}")
                continue
                
        return total_chunks

    async def run_stream(self, file_path: str) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Streaming ingestion — yields progress events at each pipeline stage.
        """
        run_start = time.time()
        
        try:
            # ── Stage 1: Load ──
            yield {"event": "status", "data": {"step": "loading", "message": f"Loading file..."}}
            
            t0 = time.time()
            docs = Loader.load(file_path)
            load_ms = int((time.time() - t0) * 1000)
            
            yield {"event": "progress", "data": {
                "step": "loaded",
                "message": f"File loaded ({len(docs)} pages)",
                "details": {"page_count": len(docs)},
                "elapsed_ms": load_ms,
            }}
            
            # ── Stage 2: Clean ──
            yield {"event": "status", "data": {"step": "cleaning", "message": "Cleaning text..."}}
            
            t0 = time.time()
            cleaned_docs = Cleaner.clean(docs)
            clean_ms = int((time.time() - t0) * 1000)
            
            yield {"event": "progress", "data": {
                "step": "cleaned",
                "message": f"Text cleaned ({len(cleaned_docs)} documents)",
                "details": {"doc_count": len(cleaned_docs)},
                "elapsed_ms": clean_ms,
            }}
            
            # ── Stage 3: Chunk ──
            yield {"event": "status", "data": {"step": "chunking", "message": "Splitting into chunks..."}}
            
            t0 = time.time()
            chunks = self.chunker.chunk(cleaned_docs)
            chunk_ms = int((time.time() - t0) * 1000)
            
            if not chunks:
                yield {"event": "error", "data": {"message": "No chunks generated from file."}}
                return
            
            yield {"event": "progress", "data": {
                "step": "chunked",
                "message": f"Split into {len(chunks)} chunks",
                "details": {"chunk_count": len(chunks)},
                "elapsed_ms": chunk_ms,
            }}
            
            # ── Stage 4: Embed ──
            yield {"event": "status", "data": {"step": "embedding", "message": f"Generating embeddings for {len(chunks)} chunks..."}}
            
            t0 = time.time()
            points = []
            for i, chunk in enumerate(chunks):
                text = chunk["content"]
                metadata = chunk["metadata"]
                
                vector = self.embedder.embed_text(text)
                point_id = str(uuid.uuid4())
                payload = {"content": text, "metadata": metadata}
                
                points.append(models.PointStruct(
                    id=point_id,
                    vector=vector,
                    payload=payload
                ))
                
                # Yield progress every 5 chunks
                if (i + 1) % 5 == 0 or i == len(chunks) - 1:
                    yield {"event": "progress", "data": {
                        "step": "embedding",
                        "message": f"Embedded {i + 1}/{len(chunks)} chunks",
                        "details": {"embedded": i + 1, "total": len(chunks)},
                    }}
            
            embed_ms = int((time.time() - t0) * 1000)
            yield {"event": "progress", "data": {
                "step": "embedded",
                "message": f"All {len(chunks)} chunks embedded",
                "details": {"chunk_count": len(chunks)},
                "elapsed_ms": embed_ms,
            }}
            
            # ── Stage 5: Upsert ──
            yield {"event": "status", "data": {"step": "upserting", "message": "Uploading to Qdrant..."}}
            
            t0 = time.time()
            self.qdrant_client.upsert(points)
            upsert_ms = int((time.time() - t0) * 1000)
            
            total_ms = int((time.time() - run_start) * 1000)
            
            yield {"event": "done", "data": {
                "step": "complete",
                "message": f"Ingestion complete! {len(points)} chunks stored.",
                "details": {
                    "chunks_processed": len(points),
                    "upsert_ms": upsert_ms,
                    "embed_ms": embed_ms,
                    "total_ms": total_ms,
                },
                "elapsed_ms": total_ms,
            }}
            
        except Exception as e:
            logger.error(f"Streaming ingestion failed: {e}")
            yield {"event": "error", "data": {"message": str(e)}}
