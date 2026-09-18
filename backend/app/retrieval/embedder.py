import logging
from typing import List
from huggingface_hub import InferenceClient
from app.core.settings import settings

logger = logging.getLogger(__name__)

class Embedder:
    def __init__(self):
        self.model_name = settings.EMBEDDING_MODEL
        self.api_key = settings.HF_TOKEN
        
        logger.info(f"Initializing HF Inference Client for model: {self.model_name}")
        try:
            self.client = InferenceClient(
                provider="hf-inference",
                api_key=self.api_key,
                model=self.model_name
            )
            # Verify basic connection/sanity check could be here, but we'll do it lazily
        except Exception as e:
            logger.error(f"Failed to initialize InferenceClient: {e}")
            raise e

    def embed_text(self, text: str) -> List[float]:
        try:
            # We use feature_extraction for embeddings
            # Note: BAAI/bge-m3 output may vary slightly depending on parameters, 
            # but default feature_extraction should work.
            # Ensure we get a flat list of floats.
            
            # The client.feature_extraction returns numpy array usually.
            response = self.client.feature_extraction(text)
            
            # If response is a list of lists (batch), take the first one?
            # Or if it's a simple array.
            # InferenceClient returns a numpy ndarray usually if numpy is installed, 
            # or a list.
            
            if hasattr(response, 'tolist'):
                 # It's a numpy array
                 return response.tolist()
            elif isinstance(response, list):
                # If it's a list of lists (e.g. [ [0.1, ...] ]), take the first.
                # If it's a plain list [0.1, ...], return it.
                if response and isinstance(response[0], list):
                    return response[0]
                return response
            
            return list(response)
            
        except Exception as e:
            logger.error(f"Failed to embed text: {e}")
            raise e

from functools import lru_cache

@lru_cache()
def get_embedder() -> Embedder:
    return Embedder()
