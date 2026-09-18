import logging
from typing import List, Optional, Dict, Any
from qdrant_client import QdrantClient as QdrantClientLib
from qdrant_client.http import models
from qdrant_client.http.exceptions import UnexpectedResponse
from app.core.settings import settings

logger = logging.getLogger(__name__)

class QdrantClientWrapper:
    def __init__(self):
        self.client = QdrantClientLib(
            url=f"https://{settings.QDRANT_HOST}:{settings.QDRANT_PORT}",
            api_key=settings.QDRANT_API_KEY if settings.QDRANT_API_KEY else None,
            timeout=60.0,
        )
        self.collection_name = settings.QDRANT_COLLECTION_NAME
        self.vector_size = settings.EMBEDDING_DIM
        self._ensure_collection_exists()

    def _ensure_collection_exists(self):
        """
        Checks if the collection exists, and if not, creates it.
        """
        try:
            # Check if collection exists
            self.client.get_collection(self.collection_name)
            logger.info(f"Connected to Qdrant collection: {self.collection_name}")
        except (UnexpectedResponse, ValueError): 
            # ValueError is raised by some versions of python client if collection not found
            # UnexpectedResponse is raised if 404
            logger.info(f"Collection {self.collection_name} not found. Creating it...")
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(
                    size=self.vector_size,
                    distance=models.Distance.COSINE
                )
            )
            logger.info(f"Created collection: {self.collection_name}")
        except Exception as e:
            logger.error(f"Failed to ensure collection exists: {e}")
            raise e

    def upsert(self, points: List[models.PointStruct]):
        """
        Upsert points into the collection.
        """
        try:
            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )
            logger.info(f"Upserted {len(points)} points into {self.collection_name}")
        except Exception as e:
            logger.error(f"Failed to upsert points: {e}")
            raise e

    def search(
        self,
        query_vector: List[float],
        limit: int = 5,
        score_threshold: Optional[float] = None,
        query_filter: Optional[models.Filter] = None
    ) -> List[Any]:
        """
        Search for similar vectors using query_points (new qdrant-client API).
        """
        try:
            result = self.client.query_points(
                collection_name=self.collection_name,
                query=query_vector,
                query_filter=query_filter,
                limit=limit,
                score_threshold=score_threshold,
            )
            return result.points
        except Exception as e:
            logger.error(f"Search failed: {e}")
            raise e
            
    def close(self):
        self.client.close()

from functools import lru_cache

@lru_cache()
def get_qdrant_client() -> QdrantClientWrapper:
    return QdrantClientWrapper()
