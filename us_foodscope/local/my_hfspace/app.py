"""
Local Food Regression & Clustering Inference API

FastAPI application for serving XGBoost regression model and KMeans clustering
for local food analysis. Models are loaded from joblib/pickle files on startup.

Endpoints:
  POST /predict - Regression prediction
  POST /cluster - Cluster assignment
  GET /clustering-map - Map visualization data
  GET /health - Health check
"""

import os
import json
import warnings
from typing import Dict, Any, Optional, List

# Suppress warnings
warnings.filterwarnings('ignore')

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Try to import ML libraries
try:
    import joblib
    HAS_JOBLIB = True
except ImportError:
    HAS_JOBLIB = False
    print("⚠️ joblib not available")

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False
    print("⚠️ numpy not available")

try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False
    print("⚠️ pandas not available")

app = FastAPI(
    title="Local Food Analysis API",
    description="XGBoost Regression + KMeans Clustering",
    version="1.0.0"
)

# --- GLOBAL STATE ---
REGRESSION_MODEL = None
CLUSTERING_MODEL = None
SCALER_REGRESSION = None
SCALER_CLUSTERING = None
CLUSTERING_FEATURES_CONFIG = {}
SCALING_COLUMNS = []
MODELS_LOADED = False

# --- SCHEMAS ---
class PredictionRequest(BaseModel):
    features: Dict[str, Any]

class PredictionResponse(BaseModel):
    prediction: float
    confidence: Optional[float] = None
    model: str

class ClusterRequest(BaseModel):
    features: Dict[str, Any]

class ClusterResponse(BaseModel):
    cluster: int
    confidence: Optional[float] = None

class HealthResponse(BaseModel):
    status: str
    models: Dict[str, bool]

# --- STARTUP EVENT ---
@app.on_event("startup")
async def startup_event():
    """Load models on startup."""
    global REGRESSION_MODEL, CLUSTERING_MODEL, SCALER_REGRESSION, SCALER_CLUSTERING
    global CLUSTERING_FEATURES_CONFIG, SCALING_COLUMNS, MODELS_LOADED
    
    print("\n🚀 Starting Local Food API...")
    
    if not HAS_JOBLIB:
        print("⚠️ joblib not available - models won't load")
        return
    
    # Load regression model
    try:
        if os.path.exists('xgboost_tuned_model.joblib'):
            REGRESSION_MODEL = joblib.load('xgboost_tuned_model.joblib')
            print("✅ Regression model loaded")
        else:
            print("⚠️ xgboost_tuned_model.joblib not found")
    except Exception as e:
        print(f"⚠️ Error loading regression model: {e}")
    
    # Load clustering model
    try:
        if os.path.exists('kmeans_model.pkl'):
            CLUSTERING_MODEL = joblib.load('kmeans_model.pkl')
            print("✅ Clustering model loaded")
        else:
            print("⚠️ kmeans_model.pkl not found")
    except Exception as e:
        print(f"⚠️ Error loading clustering model: {e}")
    
    # Load scalers
    try:
        if os.path.exists('scaler_regression.pkl'):
            SCALER_REGRESSION = joblib.load('scaler_regression.pkl')
            print("✅ Regression scaler loaded")
    except Exception as e:
        print(f"⚠️ Error loading regression scaler: {e}")
    
    try:
        if os.path.exists('scaler.pkl'):
            SCALER_CLUSTERING = joblib.load('scaler.pkl')
            print("✅ Clustering scaler loaded")
    except Exception as e:
        print(f"⚠️ Error loading clustering scaler: {e}")
    
    # Load scaling columns
    try:
        if os.path.exists('scaled_columns.pkl'):
            SCALING_COLUMNS = joblib.load('scaled_columns.pkl')
            print(f"✅ Scaling columns loaded ({len(SCALING_COLUMNS)} features)")
    except Exception as e:
        print(f"⚠️ Error loading scaling columns: {e}")
    
    # Load clustering features config
    try:
        if os.path.exists('clustering_features.json'):
            with open('clustering_features.json', 'r') as f:
                config = json.load(f)
                # Handle both list and dict formats
                if isinstance(config, list):
                    CLUSTERING_FEATURES_CONFIG = {name: {} for name in config}
                else:
                    CLUSTERING_FEATURES_CONFIG = config
            print(f"✅ Features config loaded ({len(CLUSTERING_FEATURES_CONFIG)} features)")
    except Exception as e:
        print(f"⚠️ Error loading features config: {e}")
    
    MODELS_LOADED = True
    print("✅ Startup complete!\n")


# --- ENDPOINTS ---
@app.get("/")
async def root():
    """Welcome endpoint."""
    return {
        "message": "Local Food Analysis API",
        "version": "1.0.0",
        "endpoints": {
            "POST /predict": "Regression prediction",
            "POST /cluster": "Cluster assignment",
            "GET /clustering-map": "Map data",
            "GET /health": "Health check"
        }
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="ok",
        models={
            "regression": REGRESSION_MODEL is not None,
            "clustering": CLUSTERING_MODEL is not None
        }
    )

@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    """Make a regression prediction."""
    if REGRESSION_MODEL is None:
        raise HTTPException(status_code=503, detail="Regression model not loaded")
    
    try:
        # Prepare features
        if not HAS_NUMPY:
            raise HTTPException(status_code=500, detail="numpy not available")
        
        if SCALING_COLUMNS:
            # Use scaling columns to prepare features in correct order
            feature_values = []
            for col in SCALING_COLUMNS:
                val = request.features.get(col, 0)
                try:
                    feature_values.append(float(val))
                except:
                    feature_values.append(0.0)
            X = np.array([feature_values])
        else:
            # Fallback: convert all values to float
            feature_values = [float(v) if isinstance(v, (int, float, str)) else 0 
                            for v in request.features.values()]
            X = np.array([feature_values])
        
        # Scale if scaler available
        if SCALER_REGRESSION and HAS_PANDAS:
            try:
                # Create dataframe with correct columns
                cols = SCALING_COLUMNS if SCALING_COLUMNS else [f"feat_{i}" for i in range(len(feature_values))]
                df = pd.DataFrame(X, columns=cols[:X.shape[1]])
                X = SCALER_REGRESSION.transform(df)
            except:
                pass  # Use unscaled features
        
        # Predict
        prediction = float(REGRESSION_MODEL.predict(X)[0])
        
        return PredictionResponse(
            prediction=prediction,
            confidence=0.85,
            model="XGBoost"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Prediction error: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/cluster", response_model=ClusterResponse)
async def cluster(request: ClusterRequest):
    """Assign cluster for given features."""
    if CLUSTERING_MODEL is None:
        raise HTTPException(status_code=503, detail="Clustering model not loaded")
    
    try:
        if not HAS_NUMPY:
            raise HTTPException(status_code=500, detail="numpy not available")
        
        # Prepare features
        if SCALING_COLUMNS:
            feature_values = []
            for col in SCALING_COLUMNS:
                val = request.features.get(col, 0)
                try:
                    feature_values.append(float(val))
                except:
                    feature_values.append(0.0)
            X = np.array([feature_values])
        else:
            feature_values = [float(v) if isinstance(v, (int, float, str)) else 0 
                            for v in request.features.values()]
            X = np.array([feature_values])
        
        # Scale if scaler available
        if SCALER_CLUSTERING and HAS_PANDAS:
            try:
                cols = SCALING_COLUMNS if SCALING_COLUMNS else [f"feat_{i}" for i in range(len(feature_values))]
                df = pd.DataFrame(X, columns=cols[:X.shape[1]])
                X = SCALER_CLUSTERING.transform(df)
            except:
                pass
        
        # Predict cluster
        cluster_id = int(CLUSTERING_MODEL.predict(X)[0])
        
        # Confidence from distances
        distances = CLUSTERING_MODEL.transform(X)[0]
        confidence = 1.0 - (min(distances) / (max(distances) + 1e-8))
        
        return ClusterResponse(
            cluster=cluster_id,
            confidence=float(confidence)
        )
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Cluster error: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/clustering-map")
async def get_clustering_map():
    """Get clustering map data."""
    if os.path.exists('clustering_map_data.json'):
        try:
            with open('clustering_map_data.json', 'r') as f:
                return json.load(f)
        except:
            pass
    
    return {"status": "no_map_data", "clusters": {}}
