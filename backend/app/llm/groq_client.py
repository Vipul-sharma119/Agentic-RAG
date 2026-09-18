import logging
from typing import List, Optional, Dict, Any, Union, Generator
from groq import Groq, GroqError, APIConnectionError, RateLimitError
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from app.core.settings import settings

logger = logging.getLogger(__name__)

class GroqClient:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.GROQ_API_KEY
        if not self.api_key:
            raise ValueError("GROQ_API_KEY is not set")
        
        self.client = Groq(api_key=self.api_key)
        self.model = settings.GROQ_MODEL
                                       
    @retry(
        retry=retry_if_exception_type((APIConnectionError, RateLimitError)),
        wait=wait_exponential(multiplier=1, min=2, max=60),
        stop=stop_after_attempt(5),
        reraise=True
    )
    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1024,
        tools: Optional[List[Dict[str, Any]]] = None,
        tool_choice: Optional[Union[str, Dict[str, Any]]] = "auto"
    ) -> Any:
        """
        Sends a chat completion request to Groq API with automatic retries.
        """
        target_model = model or self.model
        
        try:
            logger.info(f"Sending request to Groq (Model: {target_model})")
            
            kwargs = {
                "messages": messages,
                "model": target_model,
                "temperature": temperature,
                "max_tokens": max_tokens,
            }
            if tools:
                kwargs["tools"] = tools
                kwargs["tool_choice"] = tool_choice

            response = self.client.chat.completions.create(**kwargs)
            return response
            
        except GroqError as e:
            logger.error(f"Groq API Error: {str(e)}")
            raise e
        except Exception as e:
            logger.error(f"Unexpected error in GroqClient: {str(e)}")
            raise e

    def chat_completion_stream(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2048,
    ) -> Generator:
        """
        Streaming chat completion — yields token chunks as they arrive from Groq.
        """
        target_model = model or self.model
        
        try:
            logger.info(f"Starting streaming request to Groq (Model: {target_model})")
            stream = self.client.chat.completions.create(
                messages=messages,
                model=target_model,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=True,
            )
            return stream
        except GroqError as e:
            logger.error(f"Groq Streaming Error: {str(e)}")
            raise e
        except Exception as e:
            logger.error(f"Unexpected streaming error: {str(e)}")
            raise e

# specific instance for dependency injection if needed
groq_client = GroqClient()

def get_groq_client() -> GroqClient:
    """
    Returns the singleton GroqClient instance.
    """
    return groq_client
