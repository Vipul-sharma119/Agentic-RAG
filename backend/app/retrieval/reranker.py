from typing import List, Dict, Any
from sentence_transformers import CrossEncoder
import logging
import torch
import math

logger = logging.getLogger(__name__)


def sigmoid(x: float) -> float:
    """Convert raw logit to [0, 1] probability."""
    return 1.0 / (1.0 + math.exp(-x))


class Reranker:
    def __init__(self, model_name: str = "cross-encoder/ms-marco-TinyBERT-L-2-v2"):
        self.model_name = model_name
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"Loading reranking model: {self.model_name} on {self.device}")
        try:
            self.model = CrossEncoder(self.model_name, device=self.device)
        except Exception as e:
            logger.error(f"Failed to load reranking model {self.model_name}: {e}")
            raise e

    def rerank(self, query: str, docs: List[Dict[str, Any]], top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Reranks documents using cross-encoder scoring with sigmoid normalization.
        
        Scoring Pipeline:
        1. Raw cross-encoder logit (range: ~-10 to +10)
        2. Sigmoid normalization → [0, 1] relevance probability
        3. Composite score = 0.3 * norm_retrieval + 0.7 * norm_rerank
        4. Sort descending by composite score
        """
        if not docs:
            return []

        sentence_pairs = [[query, doc.get("content", "")] for doc in docs]
        
        try:
            # Get raw cross-encoder scores
            raw_scores = self.model.predict(sentence_pairs)
            
            # Normalize retrieval scores (Qdrant cosine similarity, range: ~0 to 1)
            max_retrieval = max((doc.get("score", 0) for doc in docs), default=1) or 1
            
            for i, doc in enumerate(docs):
                raw_rerank = float(raw_scores[i])
                norm_rerank = sigmoid(raw_rerank)
                norm_retrieval = doc.get("score", 0) / max_retrieval if max_retrieval > 0 else 0
                
                # Composite score: reranker is more trustworthy than raw embedding similarity
                composite = 0.3 * max(norm_retrieval, 0) + 0.7 * norm_rerank
                
                doc["raw_rerank_score"] = round(raw_rerank, 4)
                doc["rerank_score"] = round(norm_rerank, 4)
                doc["retrieval_score"] = round(doc.get("score", 0), 4)
                doc["composite_score"] = round(composite, 4)
                
                logger.debug(
                    f"Doc {i}: retrieval={doc['retrieval_score']:.4f} → "
                    f"raw_rerank={raw_rerank:.4f} → norm_rerank={norm_rerank:.4f} → "
                    f"composite={composite:.4f}"
                )
                
            # Sort by composite score descending
            reranked_docs = sorted(docs, key=lambda x: x["composite_score"], reverse=True)
            
            logger.info(
                f"Reranked {len(docs)} docs. "
                f"Top score: {reranked_docs[0]['composite_score']:.4f}, "
                f"Bottom score: {reranked_docs[-1]['composite_score']:.4f}"
            )
            
            return reranked_docs[:top_k]
            
        except Exception as e:
            logger.error(f"Reranking failed: {e}")
            return docs[:top_k]


def get_reranker() -> Reranker:
    return Reranker()
