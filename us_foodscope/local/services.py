"""
Local Food Prediction Service

Communicates with Hugging Face Space for regression and clustering predictions.
Includes fallback mock predictions for development/testing.
"""

import requests
from django.conf import settings
from typing import Dict, Any, Optional
import logging
import random

logger = logging.getLogger(__name__)


class LocalFoodPredictionService:
    """
    Service to handle communication with the external ML Inference API
    hosted on Hugging Face Spaces for local food analysis.
    
    Endpoint: https://rouazekri-roua-localfood.hf.space
    
    Falls back to mock predictions if API is unavailable.
    """
    
    # Default to HF Space - can be overridden via settings
    HF_API_URL = getattr(settings, 'LOCAL_FOOD_HF_API_URL', 'https://rouazekri-roua-localfood.hf.space')
    
    @classmethod
    def predict(cls, features: Dict[str, Any]) -> Dict[str, Any]:
        """
        Send prediction request to the HF Space for regression.
        
        Args:
            features: Dictionary of raw feature inputs
            
        Returns:
            Dict containing 'prediction', 'confidence', 'model_used'
        """
        endpoint = f"{cls.HF_API_URL}/predict"
        
        payload = {
            "features": features
        }
        
        logger.info(f"Sending prediction request to: {endpoint}")
        logger.info(f"Payload keys: {list(payload.keys())}")
        
        try:
            response = requests.post(endpoint, json=payload, timeout=30.0)
            
            logger.info(f"Response status code: {response.status_code}")
            logger.info(f"Response content-type: {response.headers.get('content-type', 'Not set')}")
            
            # Check if response is JSON
            if 'application/json' not in response.headers.get('content-type', ''):
                logger.warning(f"Invalid content-type: {response.headers.get('content-type')}")
                logger.warning(f"Response text: {response.text[:200]}")
                return cls._mock_prediction(features)
            
            response.raise_for_status()
            result = response.json()
            
            logger.info(f"API returned: {result}")
            
            if "error" in result:
                logger.warning(f"API returned error: {result['error']}")
                return cls._mock_prediction(features)
            
            return result
            
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP Error in prediction: {e.response.status_code}")
            return cls._mock_prediction(features)
        except requests.exceptions.JSONDecodeError as e:
            logger.error(f"JSON Decode Error: {str(e)}")
            return cls._mock_prediction(features)
        except requests.exceptions.RequestException as e:
            logger.error(f"Local Food Prediction API Error: {str(e)}")
            return cls._mock_prediction(features)
    
    @classmethod
    def predict_cluster(cls, features: Dict[str, Any]) -> Dict[str, Any]:
        """
        Send request to get cluster assignment.
        
        Args:
            features: Dictionary of raw feature inputs
            
        Returns:
            Dict containing 'cluster', 'confidence'
        """
        endpoint = f"{cls.HF_API_URL}/cluster"
        
        payload = {
            "features": features
        }
        
        logger.info(f"Sending cluster request to: {endpoint}")
        
        try:
            response = requests.post(endpoint, json=payload, timeout=30.0)
            
            logger.info(f"Cluster response status code: {response.status_code}")
            logger.info(f"Cluster response content-type: {response.headers.get('content-type', 'Not set')}")
            
            # Check if response is JSON
            if 'application/json' not in response.headers.get('content-type', ''):
                logger.warning(f"Invalid content-type: {response.headers.get('content-type')}")
                return cls._mock_cluster(features)
            
            response.raise_for_status()
            result = response.json()
            
            logger.info(f"Cluster API returned: {result}")
            
            if "error" in result:
                logger.warning(f"API returned error: {result['error']}")
                return cls._mock_cluster(features)
            
            return result
            
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP Error in clustering: {e.response.status_code}")
            return cls._mock_cluster(features)
        except requests.exceptions.JSONDecodeError as e:
            logger.error(f"JSON Decode Error: {str(e)}")
            return cls._mock_cluster(features)
        except requests.exceptions.RequestException as e:
            logger.error(f"Local Food Clustering API Error: {str(e)}")
            return cls._mock_cluster(features)
    
    @classmethod
    def _mock_prediction(cls, features: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate mock prediction for testing/demo purposes.
        """
        logger.info("Using mock prediction (API unavailable)")
        # Generate realistic mock value based on input
        base_value = sum(float(v) if isinstance(v, (int, float, str)) else 0 
                        for v in features.values()) / max(len(features), 1)
        prediction = 40 + (base_value % 30)
        
        return {
            "prediction": round(prediction, 2),
            "confidence": round(0.75 + random.random() * 0.2, 2),
            "model": "XGBoost (Mock)"
        }
    
    @classmethod
    def _mock_cluster(cls, features: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate mock cluster assignment for testing/demo purposes.
        """
        logger.info("Using mock clustering (API unavailable)")
        cluster_id = random.randint(0, 4)
        
        return {
            "cluster": cluster_id,
            "confidence": round(0.70 + random.random() * 0.25, 2)
        }
    
    @classmethod
    def get_clustering_map_data(cls) -> Dict[str, Any]:
        """
        Load clustering data for map visualization.
        
        Returns:
            Dict with counties and cluster information for visualization
        """
        endpoint = f"{cls.HF_API_URL}/clustering-map"
        
        try:
            response = requests.get(endpoint, timeout=5.0)
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Clustering Map API Error: {str(e)}")
            return {
                "error": "Map Data Service Unavailable",
                "details": str(e)
            }

