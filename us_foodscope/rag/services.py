import requests
from django.conf import settings
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger(__name__)

class RemoteRAGService:
    """
    Service to handle RAG queries by calling the remote Hugging Face Space API.
    This replaces the local FAISS/SentenceTransformer implementation to save memory.
    """
    
    HF_API_URL = getattr(settings, 'HF_API_URL', 'https://edamhakim-us-foodscope.hf.space')

    def __init__(self):
        self.initialized = True  # Remote service is always "initialized" if URL is set

    def generate_response(self, query: str) -> Dict[str, Any]:
        """
        Send a query to the remote RAG endpoint.
        """
        endpoint = f"{self.HF_API_URL}/ask"
        payload = {"query": query}
        
        try:
            # Short timeout to prevent hanging the Django web request
            response = requests.post(endpoint, json=payload, timeout=15.0)
            response.raise_for_status()
            result = response.json()
            
            # Map API response format to what the Django view expects
            return {
                "response": result.get("answer"),
                "sources": result.get("sources", []),
                "error": None
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Remote RAG API Error: {str(e)}")
            return {
                "response": "The AI assistant is currently unavailable. Please try again later.",
                "sources": [],
                "error": str(e)
            }

# Singleton instance access
_rag_service = None

def get_rag_service():
    global _rag_service
    if _rag_service is None:
        _rag_service = RemoteRAGService()
    return _rag_service
