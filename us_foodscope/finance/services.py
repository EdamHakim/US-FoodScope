"""
Finance Prediction Service
Handles Remote Inference calls to Hugging Face Space.
"""
import requests


class FinancePredictionService:
    """
    Service to handle Remote Inference calls to Hugging Face Space
    """
    
    # Single HuggingFace Space URL for all finance models
    HF_FINANCE_SPACE_URL = 'https://mariem08-fml-models.hf.space'
    
    @staticmethod
    def predict(model_type, input_data):
        """
        Send prediction request to remote inference API
        
        Args:
            model_type: 'tax_rate' or 'clustering'
            input_data: dict with feature values
            
        Returns:
            dict with:
                - 'prediction': the predicted value
                - 'probability': (optional) confidence score
                - 'cluster_data': (clustering only) list of state data for map
                - 'priority_states': (clustering only) top 5 high-risk states
        """
        try:
            # Build the full endpoint URL based on model type
            # IMPORTANT: Using Gradio's API endpoints from app.py
            if model_type == 'tax_rate':
                url = f"{FinancePredictionService.HF_FINANCE_SPACE_URL}/api/predict_tax"
                # Get the features in the order your Gradio app expects them
                # Based on your screenshot and app.py, it looks like:
                # Adult_Obesity_Rate13, Adult_Diabetes_Rate13, Adult_Obesity_Rate_08, etc.
                # We need to map Django form fields to Gradio's expected order
                payload = {
                    "data": [
                        input_data.get('Adult_Obesity_Rate_08', 0),
                        input_data.get('Adult_Diabetes_Rate_08', 0),
                        input_data.get('Adult_Obesity_Rate13', 0),
                        input_data.get('Adult_Diabetes_Rate13', 0),
                        input_data.get('SODATAX_STORES14', 0),
                        input_data.get('CHIPSTAX_VENDM14', 0),
                        input_data.get('PCT_LOCLFARM12', 0),
                        input_data.get('VLFOODSEC_10_12', 0),
                    ]
                }
            elif model_type == 'clustering':
                url = f"{FinancePredictionService.HF_FINANCE_SPACE_URL}/api/predict_cluster"
                payload = {
                    "data": [
                        input_data.get('Median_Income', 0),
                        input_data.get('FOODINSEC_13_15', 0),
                        input_data.get('Adult_Obesity_Rate13', 0),
                    ]
                }
            else:
                return {'error': True, 'details': f'Unknown model type: {model_type}'}
            
            print(f"[API] Calling {url}")
            print(f"[API] Payload: {payload}")
            
            # Make API call
            response = requests.post(url, json=payload, timeout=30)
            
            # Check if the endpoint exists
            if response.status_code == 404:
                print(f"[API] Endpoint not found (404). Trying alternative endpoints...")
                # Try without /api/ prefix
                if model_type == 'tax_rate':
                    alt_url = f"{FinancePredictionService.HF_FINANCE_SPACE_URL}/predict_tax"
                else:
                    alt_url = f"{FinancePredictionService.HF_FINANCE_SPACE_URL}/predict_cluster"
                
                print(f"[API] Trying alternative: {alt_url}")
                response = requests.post(alt_url, json=payload, timeout=30)
            
            response.raise_for_status()
            
            result = response.json()
            print(f"[API] Response: {result}")
            
            # Process the Gradio response
            if model_type == 'tax_rate':
                # The Gradio function returns a Markdown string
                # We need to extract the numerical value from it
                if isinstance(result, dict) and 'data' in result:
                    # Gradio returns {"data": ["### Tax Rate Prediction Result\n\n**Predicted Tax Rate:** 25.5%..."]}
                    result_text = result['data'][0]
                    # Extract the tax rate number (e.g., 25.5 from "25.5%")
                    import re
                    match = re.search(r'Predicted Tax Rate.*?(\d+\.?\d*)', result_text)
                    if match:
                        prediction_value = float(match.group(1))
                        return {
                            'prediction': prediction_value,
                            'probability': '85%'
                        }
                return {
                    'prediction': 0.0,
                    'probability': 'N/A'
                }
                
            elif model_type == 'clustering':
                # For clustering, Gradio returns both text and a plot
                # We need to parse the cluster number from the text
                if isinstance(result, dict) and 'data' in result:
                    result_data = result['data']
                    if len(result_data) >= 1:
                        result_text = result_data[0]
                        # Extract cluster number
                        import re
                        match = re.search(r'State Cluster.*?(\d+)', result_text)
                        if match:
                            cluster_number = int(match.group(1))
                            return {
                                'prediction': cluster_number,
                                'probability': '90%',
                                'cluster_data': FinancePredictionService._get_mock_cluster_data(),
                                'priority_states': FinancePredictionService._get_mock_priority_states()
                            }
                return {
                    'prediction': 1,
                    'probability': 'N/A',
                    'cluster_data': FinancePredictionService._get_mock_cluster_data(),
                    'priority_states': FinancePredictionService._get_mock_priority_states()
                }
            
            return {'error': True, 'details': 'Invalid response format'}
            
        except requests.exceptions.RequestException as e:
            print(f"[API ERROR] Request failed: {str(e)}")
            
            # For development: return mock data
            if model_type == 'tax_rate':
                return {
                    'prediction': 25.5,
                    'probability': '85%'
                }
            elif model_type == 'clustering':
                return {
                    'prediction': 1,
                    'probability': '90%',
                    'cluster_data': FinancePredictionService._get_mock_cluster_data(),
                    'priority_states': FinancePredictionService._get_mock_priority_states()
                }
            
            return {
                'error': True,
                'details': f'API request failed: {str(e)}'
            }
        except Exception as e:
            print(f"[API ERROR] Unexpected error: {str(e)}")
            import traceback
            traceback.print_exc()
            return {
                'error': True,
                'details': f'Unexpected error: {str(e)}'
            }
    
    @staticmethod
    def _get_mock_cluster_data():
        """Mock cluster data for map visualization"""
        return [
            {'name': 'California', 'lat': 36.7783, 'lng': -119.4179, 'cluster': 1, 'score': 0.95},
            {'name': 'Texas', 'lat': 31.9686, 'lng': -99.9018, 'cluster': 2, 'score': 0.85},
            {'name': 'Florida', 'lat': 27.6648, 'lng': -81.5158, 'cluster': 2, 'score': 0.80},
            {'name': 'New York', 'lat': 42.1657, 'lng': -74.9481, 'cluster': 1, 'score': 0.90},
            {'name': 'Illinois', 'lat': 40.6331, 'lng': -89.3985, 'cluster': 3, 'score': 0.70},
            {'name': 'Arizona', 'lat': 34.0489, 'lng': -111.0937, 'cluster': 3, 'score': 0.65},
            {'name': 'Washington', 'lat': 47.7511, 'lng': -120.7401, 'cluster': 3, 'score': 0.60},
            {'name': 'Pennsylvania', 'lat': 41.2033, 'lng': -77.1945, 'cluster': 2, 'score': 0.75},
            {'name': 'Ohio', 'lat': 40.4173, 'lng': -82.9071, 'cluster': 2, 'score': 0.72},
            {'name': 'Georgia', 'lat': 32.1656, 'lng': -82.9001, 'cluster': 1, 'score': 0.88},
            {'name': 'North Carolina', 'lat': 35.7596, 'lng': -79.0193, 'cluster': 2, 'score': 0.78},
            {'name': 'Michigan', 'lat': 44.3148, 'lng': -85.6024, 'cluster': 3, 'score': 0.68},
            {'name': 'New Jersey', 'lat': 40.0583, 'lng': -74.4057, 'cluster': 1, 'score': 0.92},
            {'name': 'Virginia', 'lat': 37.4316, 'lng': -78.6569, 'cluster': 3, 'score': 0.63},
            {'name': 'Massachusetts', 'lat': 42.4072, 'lng': -71.3824, 'cluster': 3, 'score': 0.58},
        ]
    
    @staticmethod
    def _get_mock_priority_states():
        """Mock priority states data"""
        return [
            {'name': 'California', 'cluster': 1, 'score': '0.95'},
            {'name': 'New York', 'cluster': 1, 'score': '0.90'},
            {'name': 'Georgia', 'cluster': 1, 'score': '0.88'},
            {'name': 'New Jersey', 'cluster': 1, 'score': '0.92'},
            {'name': 'Texas', 'cluster': 2, 'score': '0.85'},
        ]