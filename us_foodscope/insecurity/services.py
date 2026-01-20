"""
Service Layer for Insecurity App

Handles food insecurity predictions and clustering data retrieval.
"""

from django.conf import settings
from .ml_loader import ml_loader
import numpy as np


class FoodInsecurityPredictionService:
    """
    Service to handle food insecurity risk predictions using the trained RandomForest model.
    """
    
    @classmethod
    def predict(cls, features: dict) -> dict:
        """
        Predict food insecurity risk for given county features.
        
        Args:
            features: Dictionary of feature values matching the model's expected features
            
        Returns:
            Dict containing 'prediction', 'risk_level', 'confidence'
        """
        try:
            # Check if models are loaded
            if not ml_loader.has_model('random_forest'):
                return {
                    'error': 'Prediction model not available',
                    'details': 'RandomForest model not loaded'
                }
            
            if not ml_loader.has_model('scaler_prediction'):
                return {
                    'error': 'Scaler not available',
                    'details': 'Feature scaler not loaded'
                }
            
            # Get models
            rf_model = ml_loader.get_model('random_forest')
            scaler = ml_loader.get_model('scaler_prediction')
            metadata = ml_loader.get_metadata()
            feature_names = metadata.get('feature_names', [])
            
            # If no feature names in metadata, use the form field names
            if not feature_names:
                feature_names = [
                    'PCT_LACCESS_POP15', 'LACCESS_BLACK15', 'LACCESS_HISP15',
                    'LACCESS_NHASIAN15', 'Poverty_Rate', 'Adult_Obesity_Rate13',
                    'Adult_Diabetes_Rate13', 'FOODINSEC_13_15'
                ]
            
            # Prepare feature vector in correct order
            X = np.array([[features.get(f, 0) for f in feature_names]])
            
            # Scale features
            X_scaled = scaler.transform(X)
            
            # Make prediction
            prediction = rf_model.predict(X_scaled)[0]
            
            # Get prediction confidence (using prediction variance from ensemble)
            try:
                predictions_all = np.array([tree.predict(X_scaled)[0] for tree in rf_model.estimators_])
                std_dev = np.std(predictions_all)
                confidence = max(0, min(1, 1 - (std_dev / (abs(prediction) + 1e-6))))
            except:
                confidence = 0.7  # Default confidence if calculation fails
            
            # Determine risk level based on prediction
            if prediction < 0.3:
                risk_level = 'Low'
                risk_color = '#9ecae1'  # Blue for low risk
            elif prediction < 0.6:
                risk_level = 'Medium'
                risk_color = '#fc9272'  # Orange for medium risk
            else:
                risk_level = 'High'
                risk_color = '#de2d26'  # Red for high risk
            
            return {
                'prediction': float(prediction),
                'risk_level': risk_level,
                'risk_color': risk_color,
                'confidence': float(confidence),
                'model_used': 'RandomForestRegressor',
                'features_used': len(feature_names)
            }
            
        except Exception as e:
            print(f"Prediction Error: {str(e)}")
            import traceback
            traceback.print_exc()
            return {
                'error': 'Prediction failed',
                'details': str(e)
            }


class ClusteringDataService:
    """
    Service to handle clustering data retrieval and formatting.
    """
    
    @classmethod
    def get_clustering_info(cls, county_name: str, state: str) -> dict:
        """
        Get clustering information for a specific county.
        
        Args:
            county_name: Name of the county
            state: State abbreviation (e.g., 'CA', 'NY')
            
        Returns:
            Dict with cluster info or None if county not found
        """
        try:
            if not ml_loader.has_model('kmeans'):
                return None
            
            # This would need to query the CSV file or database
            # For now, return basic structure
            return {
                'county': county_name,
                'state': state,
                'cluster': 0,
                'risk_label': 'Baseline'
            }
            
        except Exception as e:
            print(f"Clustering lookup error: {e}")
            return None
    
    @classmethod
    def get_model_performance(cls) -> dict:
        """
        Get the trained model's performance metrics.
        """
        metadata = ml_loader.get_metadata()
        return metadata.get('model_performance', {})
    
    @classmethod
    def get_clustering_summary(cls) -> dict:
        """
        Get summary statistics about the clustering model.
        """
        return {
            'algorithm': 'K-Means',
            'n_clusters': 2,
            'features': ml_loader.get_clustering_features(),
            'cluster_labels': [
                'Baseline (Typical food access)',
                'High Structural Food Access Vulnerability'
            ]
        }


class ClusteringDataService:
    """
    Service to handle clustering data retrieval and formatting.
    """
    
    @classmethod
    def get_clustering_info(cls, county_name: str, state: str) -> dict:
        """
        Get clustering information for a specific county.
        
        Args:
            county_name: Name of the county
            state: State abbreviation (e.g., 'CA', 'NY')
            
        Returns:
            Dict with cluster info or None if county not found
        """
        try:
            if not ml_loader.has_model('kmeans'):
                return None
            
            # This would need to query the CSV file or database
            # For now, return basic structure
            return {
                'county': county_name,
                'state': state,
                'cluster': 0,
                'risk_label': 'Baseline'
            }
            
        except Exception as e:
            print(f"Clustering lookup error: {e}")
            return None
    
    @classmethod
    def get_model_performance(cls) -> dict:
        """
        Get the trained model's performance metrics.
        """
        metadata = ml_loader.get_metadata()
        return metadata.get('model_performance', {})
    
    @classmethod
    def get_clustering_summary(cls) -> dict:
        """
        Get summary statistics about the clustering model.
        """
        return {
            'algorithm': 'K-Means',
            'n_clusters': 2,
            'features': ml_loader.get_clustering_features(),
            'cluster_labels': [
                'Baseline (Typical food access)',
                'High Structural Food Access Vulnerability'
            ]
        }
