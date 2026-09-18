import re
from typing import Tuple

class Guardrails:
    def __init__(self):
        self.blocked_terms = ["ignore all instructions", "system prompt", "drop table"]

    def validate_query(self, query: str) -> Tuple[bool, str]:
        """
        Validates the user query.
        Returns (is_valid, reason).
        """
        if not query or len(query.strip()) == 0:
            return False, "Query cannot be empty."
        
        if len(query) > 1000:
            return False, "Query content is too long."
            
        for term in self.blocked_terms:
            if term.lower() in query.lower():
                return False, f"Query contains blocked content: {term}"
                
        return True, ""

def get_guardrails() -> Guardrails:
    return Guardrails()
