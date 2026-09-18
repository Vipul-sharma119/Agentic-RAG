from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from abc import ABC, abstractmethod
from app.retrieval.retriever import get_retriever
from app.retrieval.reranker import get_reranker
import logging

logger = logging.getLogger(__name__)

class ToolInput(BaseModel):
    args: Dict[str, Any]

class BaseTool(ABC):
    name: str
    description: str
    
    @abstractmethod
    def run(self, **kwargs) -> Any:
        pass
    
    def to_schema(self) -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self._get_parameters()
            }
        }
    
    def _get_parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {},
            "required": []
        }

class RetrievalTool(BaseTool):
    name = "retrieve_documents"
    description = "Retrieve relevant documents from the knowledge base. Use this to find information about the user's query."

    def __init__(self):
        self.retriever = get_retriever()
        self.reranker = get_reranker()

    def _get_parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "The search query to retrieve relevant documents for"}
            },
            "required": ["query"]
        }

    def run(self, query: str, top_k: int = 5) -> str:
        """
        Retrieves and reranks documents. Returns formatted string with scoring transparency.
        """
        try:
            # Retrieve from vector store
            docs = self.retriever.retrieve(query, limit=top_k * 2)
            
            # Rerank with cross-encoder + sigmoid normalization
            reranked_docs = self.reranker.rerank(query, docs, top_k=top_k)
            
            # Format with scoring details
            result_str = ""
            for i, doc in enumerate(reranked_docs):
                composite = doc.get('composite_score', 0)
                retrieval = doc.get('retrieval_score', 0)
                rerank = doc.get('rerank_score', 0)
                content = doc.get('content', '')
                
                result_str += (
                    f"Document {i+1} [Relevance: {composite:.2f}] "
                    f"(retrieval: {retrieval:.3f}, rerank: {rerank:.3f}):\n"
                    f"{content}\n\n"
                )
            
            if not result_str:
                return "No relevant documents found."
                
            return result_str
            
        except Exception as e:
            logger.error(f"Retrieval tool error: {e}")
            return f"Error retrieving documents: {e}"

class CalculatorTool(BaseTool):
    name = "calculator"
    description = "Perform basic arithmetic operations."
    
    def _get_parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "expression": {"type": "string", "description": "The arithmetic expression to evaluate, e.g. '2 + 3 * 4'"}
            },
            "required": ["expression"]
        }
    
    def run(self, expression: str) -> str:
        try:
            allowed = set("0123456789+-*/(). ")
            if not all(c in allowed for c in expression):
                return "Invalid expression. Only arithmetic details allowed."
            
            return str(eval(expression))
        except Exception as e:
            return f"Error calculating: {e}"

class FinalAnswerTool(BaseTool):
    name = "final_answer"
    description = "Provide the final answer to the user. Use this tool when you have sufficient information."
    
    def _get_parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "answer": {"type": "string", "description": "The final response to the user's query"}
            },
            "required": ["answer"]
        }
    
    def run(self, answer: str) -> str:
        return answer

def get_tools() -> List[BaseTool]:
    return [RetrievalTool(), CalculatorTool(), FinalAnswerTool()]
