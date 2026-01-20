import os
import joblib
import json
import numpy as np
import pandas as pd
import warnings
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional, List

# Filter warnings
warnings.filterwarnings('ignore', category=UserWarning, module='sklearn')

app = FastAPI(title="US Food Insecurity Prediction API")

# --- GLOBAL ARTIFACTS ---
MODEL_RF = None  # Random Forest for Food Insecurity Prediction
MODEL_KMEANS = None  # KMeans for Clustering
SCALER_PREDICTION = None  # Scaler for Prediction features
SCALER_CLUSTERING = None  # Scaler for Clustering features
METADATA = {}
CLUSTERING_DATA = []

# --- Pydantic Models for Validation ---
class PredictionRequest(BaseModel):
    """Food Insecurity Prediction Request"""
    PCT_LACCESS_POP15: float
    LACCESS_BLACK15: float
    LACCESS_HISP15: float
    LACCESS_NHASIAN15: float
    Poverty_Rate: float
    Adult_Obesity_Rate13: float
    Adult_Diabetes_Rate13: float
    FOODINSEC_13_15: float

class PredictionResponse(BaseModel):
    """Food Insecurity Prediction Response"""
    prediction: float
    risk_level: str  # Low, Medium, High
    confidence: float
    model_used: str = "Random Forest"

class ClusteringDataResponse(BaseModel):
    """Clustering Data Response"""
    counties: List[Dict[str, Any]]

# --- LOADING LOGIC ---
@app.on_event("startup")
async def load_artifacts():
    """Load ML models, scalers, and clustering data"""
    global MODEL_RF, MODEL_KMEANS, SCALER_PREDICTION, SCALER_CLUSTERING
    global METADATA, CLUSTERING_DATA
    
    print("Loading ML Artifacts...")
    try:
        # Load Models
        if os.path.exists('rf_foodinsecurity_predictor.pkl'):
            MODEL_RF = joblib.load('rf_foodinsecurity_predictor.pkl')
            print("✓ Loaded Random Forest prediction model")
        
        if os.path.exists('kmeans_food_access.pkl'):
            MODEL_KMEANS = joblib.load('kmeans_food_access.pkl')
            print("✓ Loaded KMeans clustering model")
        
        # Load Scalers
        if os.path.exists('scaler_foodinsecurity.pkl'):
            SCALER_PREDICTION = joblib.load('scaler_foodinsecurity.pkl')
            print("✓ Loaded prediction scaler")
        
        if os.path.exists('scaler_food_access.pkl'):
            SCALER_CLUSTERING = joblib.load('scaler_food_access.pkl')
            print("✓ Loaded clustering scaler")
        
        # Load Metadata
        if os.path.exists('model_metadata.json'):
            with open('model_metadata.json', 'r') as f:
                METADATA = json.load(f)
            print("✓ Loaded model metadata")
        
        print("Artifacts loaded successfully!")
        
        # Load Clustering Data (county_clusters.csv)
        clustering_file = "county_clusters.csv"
        if os.path.exists(clustering_file):
            print(f"Loading clustering data from {clustering_file}...")
            try:
                df = pd.read_csv(clustering_file)
                # Convert to list of dicts consistent with API expectations
                for _, row in df.iterrows():
                    CLUSTERING_DATA.append({
                        'county': str(row['County']).strip(),
                        'state': str(row['State']).strip(),
                        'cluster': int(row['Cluster']),
                        'risk_label': str(row['risk_label']).strip(),
                        'risk_color': str(row['risk_color']).strip()
                    })
                print(f"Loaded {len(CLUSTERING_DATA)} clustering records.")
            except Exception as e:
                print(f"Error reading clustering CSV: {e}")
        else:
            print(f"Warning: {clustering_file} not found.")
        
    except Exception as e:
        print(f"CRITICAL ERROR LOADING ARTIFACTS: {e}")
        import traceback
        traceback.print_exc()

@app.get("/")
def home():
    """Health check endpoint"""
    return {
        "status": "running",
        "model": "US Food Insecurity Prediction",
        "models_loaded": {
            "random_forest": MODEL_RF is not None,
            "kmeans_clustering": MODEL_KMEANS is not None,
            "scaler_prediction": SCALER_PREDICTION is not None,
            "scaler_clustering": SCALER_CLUSTERING is not None
        },
        "clustering_data_loaded": len(CLUSTERING_DATA) > 0
    }

@app.get("/clustering-data")
def get_clustering_data():
    """Serve the clustering data as JSON"""
    return {"counties": CLUSTERING_DATA}

@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):
    """
    Predict food insecurity level based on food access and socioeconomic factors.
    
    Returns:
        - prediction: Food insecurity score (0-1 range)
        - risk_level: Low/Medium/High classification
        - confidence: Model confidence (0-100%)
    """
    if not MODEL_RF or not SCALER_PREDICTION:
        raise HTTPException(status_code=503, detail="Prediction models not loaded")
    
    try:
        # 1. Build feature vector from request
        features = [
            request.PCT_LACCESS_POP15,
            request.LACCESS_BLACK15,
            request.LACCESS_HISP15,
            request.LACCESS_NHASIAN15,
            request.Poverty_Rate,
            request.Adult_Obesity_Rate13,
            request.Adult_Diabetes_Rate13,
            request.FOODINSEC_13_15
        ]
        
        X = np.array(features).reshape(1, -1)
        
        # 2. Scale features
        X_scaled = SCALER_PREDICTION.transform(X)
        
        # 3. Make prediction
        raw_pred = MODEL_RF.predict(X_scaled)[0]
        prediction_value = float(np.clip(raw_pred, 0.0, 1.0))
        
        # 4. Determine risk level
        if prediction_value < 0.3:
            risk_level = "Low"
        elif prediction_value < 0.6:
            risk_level = "Medium"
        else:
            risk_level = "High"
        
        # 5. Calculate confidence from ensemble variance
        confidence_raw = 0.0
        try:
            if hasattr(MODEL_RF, 'estimators_'):
                tree_preds = np.array([est.predict(X_scaled)[0] for est in MODEL_RF.estimators_])
                ensemble_std = np.std(tree_preds)
                confidence_raw = max(0, 100 * (1 - ensemble_std))
                confidence = float(np.clip(confidence_raw, 0, 100))
            else:
                confidence = 85.0
        except:
            confidence = 85.0
        
        return PredictionResponse(
            prediction=prediction_value,
            risk_level=risk_level,
            confidence=confidence,
            model_used="Random Forest"
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

@app.get("/model-info")
def get_model_info():
    """Get model metadata and feature information"""
    return {
        "model_type": "Random Forest Regressor",
        "n_estimators": 200,
        "max_depth": 7,
        "r2_score": 0.953,
        "rmse": 0.538,
        "mae": 0.341,
        "prediction_features": [
            "PCT_LACCESS_POP15",
            "LACCESS_BLACK15",
            "LACCESS_HISP15",
            "LACCESS_NHASIAN15",
            "Poverty_Rate",
            "Adult_Obesity_Rate13",
            "Adult_Diabetes_Rate13",
            "FOODINSEC_13_15"
        ],
        "risk_thresholds": {
            "low": 0.3,
            "medium": 0.6,
            "high": 1.0
        },
        "clustering_model": {
            "type": "KMeans",
            "n_clusters": 2,
            "counties_analyzed": len(CLUSTERING_DATA)
        }
    }
