"""
ML Model Loader for Insecurity App

Loads pre-trained ML models:
- Clustering: KMeans model and scaler for food access vulnerability analysis
- Prediction: RandomForest model and scaler for food insecurity risk prediction

Works directly with HuggingFace repo (`belkisboufeid`) and caches in /tmp.
"""

import os
import joblib
import requests
from io import BytesIO

# HuggingFace repo base URL
HF_BASE = "https://huggingface.co/spaces/belkisboufeid/US_FoodScope/resolve/main"

# Temporary folder for caching downloaded models
TMP_DIR = "/tmp/insecurity_models"
os.makedirs(TMP_DIR, exist_ok=True)


class InsecurityMLLoader:
    """Singleton loader for insecurity app ML models."""

    _instance = None
    _models = {}
    _metadata = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_models()
        return cls._instance

    def _download_and_load(self, filename):
        """
        Download file from HF if not cached in /tmp, then load via joblib.
        """
        local_path = os.path.join(TMP_DIR, filename)

        # Download if not exists
        if not os.path.exists(local_path):
            url = f"{HF_BASE}/{filename}"
            print(f"⏳ Downloading {filename} from HuggingFace...")
            r = requests.get(url, timeout=30)
            r.raise_for_status()
            with open(local_path, "wb") as f:
                f.write(r.content)
            print(f"✓ {filename} cached in /tmp")

        # Load model via joblib
        return joblib.load(local_path)

    def _load_models(self):
        """Load all models and metadata from HF repo."""
        try:
            # Clustering models
            self._models['kmeans'] = self._download_and_load("kmeans_food_access.pkl")
            self._models['scaler_clustering'] = self._download_and_load("scaler_food_access.pkl")

            # Prediction models
            self._models['random_forest'] = self._download_and_load("rf_foodinsecurity_predictor.pkl")
            self._models['scaler_prediction'] = self._download_and_load("scaler_foodinsecurity.pkl")

            # Metadata JSON
            metadata_url = f"{HF_BASE}/model_metadata.json"
            print("⏳ Downloading model metadata...")
            r = requests.get(metadata_url, timeout=30)
            r.raise_for_status()
            self._metadata = r.json()
            print("✓ Metadata loaded")

            print("✓ All ML models loaded successfully")

        except Exception as e:
            print(f"❌ ML loading failed: {e}")
            import traceback
            traceback.print_exc()

    # Public API
    def get_model(self, model_name):
        return self._models.get(model_name)

    def has_model(self, model_name):
        return model_name in self._models

    def get_metadata(self):
        return self._metadata

    def get_feature_names(self):
        return self._metadata.get('feature_names', [])

    def get_clustering_features(self):
        # Hard-coded features for clustering
        return [
            'PCT_LACCESS_POP15',
            'LACCESS_BLACK15',
            'LACCESS_HISP15',
            'LACCESS_NHASIAN15',
            'Poverty_Rate',
            'Adult_Obesity_Rate13',
            'Adult_Diabetes_Rate13',
            'FOODINSEC_13_15'
        ]


# Singleton instance – use everywhere
ml_loader = InsecurityMLLoader()
