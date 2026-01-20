# US Food Insecurity Prediction API

FastAPI-based inference server for food insecurity prediction and county clustering analysis. Deploy to Hugging Face Spaces.

## Overview

This API provides:
- **Prediction Endpoint**: Predicts food insecurity risk levels based on food access and socioeconomic factors
- **Clustering Data**: County-level clustering analysis with risk classifications
- **Model Information**: Detailed metadata about the Random Forest and KMeans models

## Features

### Food Insecurity Prediction
- **Model**: Random Forest Regressor (200 trees, max_depth=7)
- **Performance**: R² = 0.953, RMSE = 0.538
- **Input Features** (8):
  - `PCT_LACCESS_POP15`: % of population with limited food access
  - `LACCESS_BLACK15`: Limited access for Black population
  - `LACCESS_HISP15`: Limited access for Hispanic population
  - `LACCESS_NHASIAN15`: Limited access for Asian population
  - `Poverty_Rate`: County poverty rate
  - `Adult_Obesity_Rate13`: Adult obesity percentage
  - `Adult_Diabetes_Rate13`: Adult diabetes percentage
  - `FOODINSEC_13_15`: Food insecurity rate 2013-2015
  
- **Output**:
  - Prediction score (0-1 range)
  - Risk level (Low: <0.3, Medium: 0.3-0.6, High: >0.6)
  - Model confidence (0-100%)

### County Clustering
- **Model**: KMeans (k=2 clusters)
- **Analysis**: ~3,100 US counties
- **Features**: 8 food access vulnerability metrics
- **Output**: County-level cluster assignments and risk levels

## API Endpoints

### GET `/`
Health check endpoint
```json
{
  "status": "running",
  "model": "US Food Insecurity Prediction",
  "models_loaded": {
    "random_forest": true,
    "kmeans_clustering": true,
    "scaler_prediction": true,
    "scaler_clustering": true
  },
  "clustering_data_loaded": true
}
```

### GET `/clustering-data`
Retrieve all county clustering data
```json
{
  "counties": [
    {
      "county": "Cook",
      "state": "IL",
      "cluster": 0,
      "risk_label": "High Risk",
      "risk_color": "#d32f2f"
    }
  ]
}
```

### POST `/predict`
Predict food insecurity for a county

**Request**:
```json
{
  "PCT_LACCESS_POP15": 5.2,
  "LACCESS_BLACK15": 3.1,
  "LACCESS_HISP15": 4.8,
  "LACCESS_NHASIAN15": 2.5,
  "Poverty_Rate": 15.3,
  "Adult_Obesity_Rate13": 28.5,
  "Adult_Diabetes_Rate13": 9.2,
  "FOODINSEC_13_15": 12.4
}
```

**Response**:
```json
{
  "prediction": 0.456,
  "risk_level": "Medium",
  "confidence": 87.5,
  "model_used": "Random Forest"
}
```

### GET `/model-info`
Get detailed model metadata and feature information

## Running Locally

1. **Install dependencies**:
   ```bash
   pip install -r requirement.txt
   ```

2. **Run the server**:
   ```bash
   uvicorn app:app --host 0.0.0.0 --port 7860
   ```

3. **Access API**:
   - Docs: http://localhost:7860/docs
   - OpenAPI Schema: http://localhost:7860/openapi.json

## Deploying to Hugging Face Spaces

1. Create a new Space on Hugging Face with Docker runtime
2. Push this directory to your Spaces repo:
   ```bash
   git clone https://huggingface.co/spaces/<username>/<space-name>
   cd <space-name>
   cp -r insecurity/serving/* .
   git add .
   git commit -m "Add food insecurity prediction API"
   git push
   ```

3. Your Space will automatically build and deploy the Docker container

## Files Included

- `app.py`: FastAPI application with prediction and clustering endpoints
- `Dockerfile`: Docker configuration for HF Spaces
- `requirement.txt`: Python dependencies
- `rf_foodinsecurity_predictor.pkl`: Trained Random Forest model
- `kmeans_food_access.pkl`: Trained KMeans clustering model
- `scaler_foodinsecurity.pkl`: StandardScaler for prediction features
- `scaler_food_access.pkl`: StandardScaler for clustering features
- `model_metadata.json`: Model configuration and metadata
- `county_clusters.csv`: Pre-computed county clustering results

## Model Performance

**Random Forest Prediction Model**:
- Training R²: 0.953
- RMSE: 0.538
- MAE: 0.341
- Hyperparameters: n_estimators=200, max_depth=7

**KMeans Clustering**:
- n_clusters: 2
- Scaling: StandardScaler on 8 food access features
- County Coverage: ~3,100 US counties

## Author

US FoodScope Team - Django Food Insecurity Prediction Application

## License

MIT
