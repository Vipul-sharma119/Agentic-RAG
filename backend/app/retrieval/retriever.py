from typing import List, Dict, Any, Optional
from app.retrieval.embedder import get_embedder
from app.retrieval.qdrant_client import get_qdrant_client
from qdrant_client.http import models
import logging

logger = logging.getLogger(__name__)

class Retriever:
    def __init__(self):
        self.embedder = get_embedder()
        self.qdrant_client_wrapper = get_qdrant_client()
        self.client = self.qdrant_client_wrapper.client
        self.collection_name = self.qdrant_client_wrapper.collection_name

    def retrieve(self, query: str, limit: int = 5, score_threshold: float = 0.0) -> List[Dict[str, Any]]:
        """
        Retrieves relevant documents for a given query.
        """
        try:
            # Generate embedding for the query
            query_vector = self.embedder.embed_text(query)

            # Search in Qdrant using the wrapper's search method
            search_result = self.qdrant_client_wrapper.search(
                query_vector=query_vector,
                limit=limit,
                score_threshold=score_threshold
            )

            # Process results
            results = []
            for scored_point in search_result:
                results.append({
                    "id": scored_point.id,
                    "score": scored_point.score,
                    "content": scored_point.payload.get("content", ""),
                    "metadata": scored_point.payload.get("metadata", {})
                })
            
            logger.info(f"Retrieved {len(results)} documents for query: '{query}'")
            return results

        except Exception as e:
            logger.error(f"Error during retrieval: {e}")
            raise e

def get_retriever() -> Retriever:
    return Retriever()
