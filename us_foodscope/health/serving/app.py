import os
import joblib
import numpy as np
import pandas as pd
import warnings
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional, List

# Filter warnings
warnings.filterwarnings('ignore', category=UserWarning, module='sklearn')

from rag_service import RAGService

app = FastAPI(title="US FoodScope Inference API")

# --- GLOBAL ARTIFACTS ---
MODEL_OBESITY = None
MODEL_DIABETES = None
MODEL_KMEANS = None
SCALER = None
SCALER_CLUSTERING = None
ENCODERS = {}
ALL_FEATURE_NAMES = []
SCALER_FEATURE_NAMES = []
CLUSTERING_FEATURE_NAMES = [
    "Adult_Diabetes_Rate_08", "Adult_Diabetes_Rate13",
    "Adult_Obesity_Rate_08", "Adult_Obesity_Rate13",
    "GYMs_Per_1000_Count_14", "Farmers_Markets_Count_16", "GROCPTH09"
]
CLUSTERING_DATA = []

RAG_SERVICE = RAGService()

# --- Pydantic Models for Validation ---
class PredictionRequest(BaseModel):
    model_type: str # 'obesity' or 'diabetes'
    features: Dict[str, Any] # Raw input features

class PredictionResponse(BaseModel):
    prediction: float
    probability: Optional[str] = None
    model_used: str

class ClusteringResponse(BaseModel):
    cluster: int
    features_used: Dict[str, float]

class AskRequest(BaseModel):
    query: str

class AskResponse(BaseModel):
    answer: str
    sources: List[Dict[str, Any]]

# --- LOADING LOGIC ---
@app.on_event("startup")

async def load_artifacts():
    global MODEL_OBESITY, MODEL_DIABETES, MODEL_KMEANS, SCALER, SCALER_CLUSTERING, ENCODERS
    global ALL_FEATURE_NAMES, SCALER_FEATURE_NAMES, CLUSTERING_DATA, RAG_SERVICE
    
    print("Loading ML Artifacts...")
    print("Loading ML Artifacts...")
    
    # 1. Load Encoders
    try:
        if os.path.exists('encoders'):
            for f in os.listdir('encoders'):
                if f.endswith('_encoder.joblib'):
                    col = f.replace('_encoder.joblib', '')
                    ENCODERS[col] = joblib.load(os.path.join('encoders', f))
    except Exception as e:
        print(f"Error loading encoders: {e}")

    # 2. Load Models & Scaler
    try:
        if os.path.exists('model_obesity.joblib'):
            MODEL_OBESITY = joblib.load('model_obesity.joblib')
        if os.path.exists('model_diabetes.joblib'):
            MODEL_DIABETES = joblib.load('model_diabetes.joblib')
        if os.path.exists('standard_scaler.joblib'):
            SCALER = joblib.load('standard_scaler.joblib')
            
        # Feature names
        if hasattr(MODEL_OBESITY, 'feature_names_in_'):
            ALL_FEATURE_NAMES = list(MODEL_OBESITY.feature_names_in_)
        if hasattr(SCALER, 'feature_names_in_'):
            SCALER_FEATURE_NAMES = list(SCALER.feature_names_in_)
            
    except Exception as e:
        print(f"Error loading Base Models: {e}")

    # 3. Load Clustering Models (New)
    try:
        if os.path.exists('kmeans_health_model.joblib'):
            MODEL_KMEANS = joblib.load('kmeans_health_model.joblib')
        else:
            print("Warning: kmeans_health_model.joblib not found")
            
        if os.path.exists('clustering_scaler.joblib'):
            SCALER_CLUSTERING = joblib.load('clustering_scaler.joblib')
        else:
            print("Warning: clustering_scaler.joblib not found")
            
    except Exception as e:
        print(f"Error loading Clustering Models: {e}")

    print("Artifacts (Base/Clustering) loading attempt complete.")

    # 4. Load Clustering Data
    try:
        clustering_file = "worst_cluster_counties.csv"
        if os.path.exists(clustering_file):
            print(f"Loading clustering data from {clustering_file}...")
            df = pd.read_csv(clustering_file)
            # Convert to list of dicts consistent with Django expectations
            for _, row in df.iterrows():
                CLUSTERING_DATA.append({
                    'county': str(row['County']).strip(),
                    'state': str(row['State']).strip(),
                    'risk': float(row['composite_risk']),
                    'cluster': int(row['Cluster'])
                })
            print(f"Loaded {len(CLUSTERING_DATA)} clustering records.")
        else:
            print(f"Warning: {clustering_file} not found.")
    except Exception as e:
        print(f"Error loading clustering data: {e}")
    
    # 5. Load RAG Assets
    try:
        print("Initializing RAG Service...")
        RAG_SERVICE.initialize()
    except Exception as e:
        print(f"Error initializing RAG: {e}")

@app.get("/")
def home():
    return {
        "status": "running", 
        "models_loaded": MODEL_OBESITY is not None and MODEL_KMEANS is not None,
        "clustering_data_loaded": len(CLUSTERING_DATA) > 0
    }

@app.get("/clustering-data")
def get_clustering_data():
    """
    Serve the clustering data as JSON.
    """
    return {"counties": CLUSTERING_DATA}

@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):
    if not MODEL_OBESITY or not SCALER:
        raise HTTPException(status_code=503, detail="Models not loaded")

    try:
        # 1. Select Model
        model_type = request.model_type.lower()
        if model_type == 'obesity':
            model = MODEL_OBESITY
            target_name = "Obesity"
        elif model_type == 'diabetes':
            model = MODEL_DIABETES
            target_name = "Diabetes"
        else:
            raise HTTPException(status_code=400, detail="Invalid model_type")

        # 2. Preprocess Input (Encode & Scale)
        raw_inputs = {}
        # Union of needed features
        needed_features = set(ALL_FEATURE_NAMES) | set(SCALER_FEATURE_NAMES)
        
        for name in needed_features:
            val = request.features.get(name, 0.0)
            
            # Encode if categorical
            if name in ENCODERS:
                try:
                    # Encoders expect string mainly, but check type
                    val_str = str(val)
                    val = float(ENCODERS[name].transform([val_str])[0])
                except Exception:
                    val = 0.0 # Unknown category fallback
            else:
                 # Ensure float
                try:
                    val = float(val)
                except:
                    val = 0.0
            
            raw_inputs[name] = val

        # 3. Scaling
        if SCALER_FEATURE_NAMES:
            scaler_vector = [raw_inputs.get(name, 0.0) for name in SCALER_FEATURE_NAMES]
            X_scaler = np.array(scaler_vector).reshape(1, -1)
            X_scaled_raw = SCALER.transform(X_scaler)[0]
            
            # Map back
            scaled_map = {name: val for name, val in zip(SCALER_FEATURE_NAMES, X_scaled_raw)}
        else:
            scaled_map = raw_inputs

        # 4. Build Final Vector
        final_vector = [scaled_map.get(name, 0.0) for name in ALL_FEATURE_NAMES]
        X_final = np.array(final_vector).reshape(1, -1)

        # 5. Predict
        raw_pred = model.predict(X_final)[0]
        prediction_value = float(raw_pred)
        
        # 6. Post-Processing (Inverse Transform logic for Z-Scores)
        # Re-implementing the logic from Django app
        if abs(prediction_value) < 10.0:
            proxy = 'Adult_Obesity_Rate_08' if model_type == 'obesity' else 'Adult_Diabetes_Rate_08'
            if proxy in SCALER_FEATURE_NAMES:
                idx = SCALER_FEATURE_NAMES.index(proxy)
                mean = SCALER.mean_[idx]
                scale = SCALER.scale_[idx]
                prediction_value = (raw_pred * scale) + mean

        # 7. Confidence Interval
        prob_str = None
        if hasattr(model, 'estimators_'):
            try:
                # Optimized tree prediction
                tree_preds = [est.predict(X_final)[0] for est in model.estimators_]
                tree_arr = np.array(tree_preds)
                
                # Inverse transform trees if needed
                if abs(prediction_value) > 10.0 and abs(raw_pred) < 10.0:
                     # Same proxy check
                    proxy = 'Adult_Obesity_Rate_08' if model_type == 'obesity' else 'Adult_Diabetes_Rate_08'
                    if proxy in SCALER_FEATURE_NAMES:
                        idx = SCALER_FEATURE_NAMES.index(proxy)
                        t_mean = SCALER.mean_[idx]
                        t_scale = SCALER.scale_[idx]
                        tree_arr = (tree_arr * t_scale) + t_mean

                std_dev = np.std(tree_arr)
                lower = max(0.0, prediction_value - (1.96 * std_dev))
                upper = prediction_value + (1.96 * std_dev)
                prob_str = f"95% Confidence Interval: {lower:.1f}% - {upper:.1f}%"
            except:
                pass

        return PredictionResponse(
            prediction=prediction_value,
            probability=prob_str,
            model_used=target_name
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest):
    if not RAG_SERVICE.initialized:
        # Try initializing if not done already (e.g. if key was set after startup)
        RAG_SERVICE.initialize()
    
    result = RAG_SERVICE.ask(request.query)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    
    return AskResponse(
        answer=result["answer"],
        sources=result["sources"]
    )

@app.post("/predict-cluster", response_model=ClusteringResponse)
def predict_cluster(request: PredictionRequest):
    if not MODEL_KMEANS or not SCALER_CLUSTERING:
        raise HTTPException(status_code=503, detail="Clustering models not loaded")
        
    try:
        # 1. Extract and Validate Features
        raw_inputs = []
        features_used = {}
        
        for name in CLUSTERING_FEATURE_NAMES:
            val = request.features.get(name)
            if val is None:
                val = 0.0
            
            try:
                val = float(val)
            except:
                val = 0.0
                
            features_used[name] = val
            raw_inputs.append(val)
            
        # 2. Scale
        X_raw = np.array(raw_inputs).reshape(1, -1)
        X_scaled = SCALER_CLUSTERING.transform(X_raw)
        
        # 3. Predict
        cluster_id = int(MODEL_KMEANS.predict(X_scaled)[0])
        
        return ClusteringResponse(
            cluster=cluster_id,
            features_used=features_used
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
