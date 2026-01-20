"""
Configuration file for Local Food Module

Add this to your Django settings.py or use environment variables.
"""

# Hugging Face API Configuration
LOCAL_FOOD_HF_API_URL = "https://rouazekri-roua-localfood.hf.space"

# Model configuration
LOCAL_FOOD_MODELS = {
    'regression': {
        'name': 'XGBoost Regressor',
        'version': '1.0',
        'input_features': 'clustering_features.json',
        'timeout': 10  # seconds
    },
    'clustering': {
        'name': 'KMeans Clustering',
        'version': '1.0',
        'num_clusters': 5,
        'timeout': 10  # seconds
    }
}

# Feature validation
FEATURE_VALIDATION = {
    'strict': False,  # Set to True to validate against training feature list
    'auto_encode': True,  # Automatically encode categorical features
    'auto_scale': True,  # Automatically scale numeric features
}

# Cache configuration (optional)
CACHE_CLUSTERING_DATA = {
    'enabled': True,
    'timeout': 3600,  # 1 hour in seconds
}
