from typing import List, Dict, Any
import re

class Cleaner:
    """
    Handles cleaning of text content.
    """
    
    @staticmethod
    def clean(docs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Cleans the content of each document in the list.
        """
        cleaned_docs = []
        for doc in docs:
            content = doc.get("content", "")
            if not content:
                continue
            
            # Normalize whitespace: replace multiple spaces/newlines with single space
            # but preserve paragraph breaks?
            # For chunks, sometimes preserving structure is better. 
            # Simple approach: reduce multiple spaces to one, strip leading/trailing.
            # Maybe keep newlines for markdown structure?
            # Let's clean excessive whitespace but keep single newlines.
            
            # Replace multiple spaces with single space
            content = re.sub(r'[ \t]+', ' ', content)
            
            # Replace 3+ newlines with 2 (paragraph break)
            content = re.sub(r'\n{3,}', '\n\n', content)
            
            # Strip
            content = content.strip()
            
            cleaned_doc = doc.copy()
            cleaned_doc["content"] = content
            cleaned_docs.append(cleaned_doc)
            
        return cleaned_docs
