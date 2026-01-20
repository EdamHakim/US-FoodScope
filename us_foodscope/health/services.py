
import requests
from django.conf import settings
from typing import Dict, Any, Optional

class HealthPredictionService:
    """
    Service to handle communication with the external ML Inference API
    hosted on Hugging Face Spaces.
    
    This replaces the local loading of models to save RAM.
    """
    
    # Default to a placeholder - USER MUST CONFIGURE THIS IN .env
    # Format: https://huggingface.co/spaces/USERNAME/SPACE_NAME
    # The actual API endpoint will be /predict
    HF_API_URL = getattr(settings, 'HF_API_URL', 'http://localhost:8000') 
    
    @classmethod
    def predict(cls, model_type: str, features: Dict[str, Any]) -> Dict[str, Any]:
        """
        Send prediction request to the HF Space.
        
        Args:
            model_type: 'obesity' or 'diabetes'
            features: Dictionary of raw feature inputs
            
        Returns:
            Dict containing 'prediction', 'probability', 'model_used'
        """
        endpoint = f"{cls.HF_API_URL}/predict"
        
        payload = {
            "model_type": model_type,
            "features": features
        }
        
        try:
            # Short timeout to prevent hanging the web request
            response = requests.post(endpoint, json=payload, timeout=8.0)
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            # Log error internally here if you have logging set up
            print(f"ML API Error: {str(e)}")
            
            # Fallback or re-raise depending on requirements
            # Currently we return a structure that mimics a failure
            return {
                "details": str(e)
            }

    @classmethod
    def predict_cluster(cls, features: Dict[str, Any]) -> Dict[str, Any]:
        """
        Send clustering prediction request to the HF Space.
        
        Args:
            features: Dictionary of raw feature inputs
            
        Returns:
            Dict containing 'cluster', 'features_used' or 'error'
        """
        endpoint = f"{cls.HF_API_URL}/predict-cluster"
        
        payload = {
            "model_type": "kmeans", # Not strictly used by endpoint but good for consistency
            "features": features
        }
        
        try:
            # Short timeout
            response = requests.post(endpoint, json=payload, timeout=8.0)
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"Clustering API Error: {str(e)}")
            return {
                "error": "Clustering Service Unavailable",
                "details": str(e)
            }



def load_clustering_data():
    """
    Load clustering data from HF API.
    Returns a list of dicts: [{'county': '...', 'state': '...', 'risk': 1.23, 'cluster': 1}, ...]
    """
    # The HF_API_URL should be configured in settings (e.g., via .env)
    hf_api_url = getattr(settings, 'HF_API_URL', None)
    
    if hf_api_url:
        try:
            # Assumes endpoint /clustering-data on the HF Space
            endpoint = f"{hf_api_url}/clustering-data"
            
            # Short timeout to prevent hanging if the Space is cold/sleeping
            response = requests.get(endpoint, timeout=5.0)
            
            if response.status_code == 200:
                data = response.json()
                if 'counties' in data:
                    return data['counties']
                else:
                    print("Clustering API response missing 'counties' key")
            else:
                print(f"Clustering API returned status {response.status_code}")
                
        except Exception as e:
            print(f"Warning: Failed to fetch clustering data from API: {e}")
            
    return []
