import requests
import logging
from django.conf import settings
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class FoodEnvironmentPredictionService:
    """
    Service to handle communication with the external ML Inference API
    hosted on Hugging Face Spaces.
    
    This service sends feature data to the HF Space and receives predictions
    for grocery store density without loading models locally.
    """
    
    # Configure this in settings.py or .env
    # Format: https://huggingface.co/spaces/USERNAME/SPACE_NAME
    HF_API_URL = getattr(settings, 'HF_FOOD_ENV_API_URL', 'http://localhost:8000')
    
    @classmethod
    def predict(cls, features: Dict[str, Any]) -> Dict[str, Any]:
        """
        Send prediction request to the HF Space for grocery store density.
        
        Args:
            features: Dictionary with the following keys:
                - restaurant_category: int (1 or 2)
                - soda_price: float
                - fmrktpth16: float (Farmers Market Path %)
                - pch_grocpth_09_14: float (Change in Grocery Path %)
                - fsrpth09: float (Fast Food Path 2009 %)
                - fsrpth14: float (Fast Food Path 2014 %)
                - pct_65older10: float (Population 65+ %)
                - poploss10: float (Population Loss %)
            
        Returns:
            Dict containing:
                - success: bool
                - prediction: float (Grocery Stores Per 1000 Residents)
                - error: str (if success is False)
        
        """
        required_features = [
            'soda_price', 'fmrktpth16',
            'pch_grocpth_09_14', 'fsrpth09',
            'fsrpth14', 'pct_65older10', 'poploss10'
        ]

        cleaned_features = {k: v for k, v in features.items() if k in required_features}
        endpoint = f"{cls.HF_API_URL}/predict-grocery"

        payload = {
            "features": cleaned_features
        }

        try:
            # Send request with 10 second timeout
            logger.debug("Sending HF request to %s with payload: %s", endpoint, payload)
            print(f"[foodenv] Sending HF request to {endpoint} payload={payload}")
            response = requests.post(endpoint, json=payload, timeout=10.0)
            logger.debug("HF response status: %s", response.status_code)
            print(f"[foodenv] HF response status: {response.status_code}")
            response.raise_for_status()

            # Log raw text for debugging (truncate to reasonable length)
            raw_text = response.text
            logger.debug("HF response text: %s", raw_text[:2000])
            print(f"[foodenv] HF response text: {raw_text[:2000]}")

            try:
                result = response.json()
                logger.debug("HF parsed JSON: %s", result)
                print(f"[foodenv] HF parsed JSON: {result}")
            except ValueError:
                logger.exception("Failed to parse HF JSON response")
                print("[foodenv] Failed to parse HF JSON response")
                return {
                    "success": False,
                    "prediction": None,
                    "error": "Invalid JSON from HF Service",
                    "raw_text": raw_text
                }

            # Try to extract prediction from common keys that HF Space might return
            prediction = None
            # Common fallback keys seen in different HF Spaces / models
            candidate_keys = [
                'prediction', 'pred', 'predicted_grocpth09', 'predicted_value',
                'result', 'output', 'outputs'
            ]
            for key in candidate_keys:
                if key in result:
                    val = result.get(key)
                    # If nested structure, try to pull numeric value
                    if isinstance(val, dict):
                        # common nested names
                        for sub in ('value', 'pred', 'prediction'):
                            if sub in val:
                                prediction = val.get(sub)
                                break
                        if prediction is None:
                            # if dict maps to a single numeric-like entry, attempt to find it
                            for subk, subv in val.items():
                                try:
                                    prediction = float(subv)
                                    break
                                except Exception:
                                    continue
                    else:
                        prediction = val
                    if prediction is not None:
                        break

            # Coerce to float when possible
            pred_float = None
            try:
                if prediction is not None:
                    pred_float = float(prediction)
            except (TypeError, ValueError):
                pred_float = None

            # Return the parsed result and include raw JSON for debugging
            return {
                "success": True,
                "prediction": pred_float,
                "error": None,
                "raw": result
            }
            
        except requests.exceptions.Timeout:
            error_msg = "ML Service timeout - request took too long"
            print(f"Food Environment API Error: {error_msg}")
            return {
                "success": False,
                "prediction": None,
                "error": error_msg
            }
        
        except requests.exceptions.ConnectionError:
            error_msg = "Cannot connect to ML Service - check API URL configuration"
            print(f"Food Environment API Error: {error_msg}")
            return {
                "success": False,
                "prediction": None,
                "error": error_msg
            }
        
        except requests.exceptions.RequestException as e:
            error_msg = f"ML Service Error: {str(e)}"
            print(f"Food Environment API Error: {error_msg}")
            return {
                "success": False,
                "prediction": None,
                "error": error_msg
            }
        
        except ValueError:
            # JSON parsing error
            error_msg = "Invalid response from ML Service"
            print(f"Food Environment API Error: {error_msg}")
            return {
                "success": False,
                "prediction": None,
                "error": error_msg
            }
    
    @classmethod
    def validate_features(cls, features: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """
        Validate that all required features are present and have correct types.
        
        Returns:
            Tuple (is_valid: bool, error_message: str or None)
        """
        required_features = [
            'soda_price', 'fmrktpth16',
            'pch_grocpth_09_14', 'fsrpth09',
            'fsrpth14', 'pct_65older10', 'poploss10'
        ]
         # Filter out csrf token and other non-feature keys
        cleaned_features = {k: v for k, v in features.items() if k in required_features}
    
        # Check if all features are present
        missing_features = [f for f in required_features if f not in cleaned_features]
        if missing_features:
            return False, f"Missing features: {', '.join(missing_features)}"
        
        # Check if all values are numeric
        for feature_name, feature_value in cleaned_features.items():
            try:
                float(feature_value)
            except (ValueError, TypeError):
                return False, f"Feature '{feature_name}' must be numeric"
        return True, None  # ← IMPORTANT : retourne TOUJOURS un tuple
       
        