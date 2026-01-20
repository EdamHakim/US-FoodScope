---
title: Local Food Analysis API
emoji: 🌾
colorFrom: green
colorTo: blue
sdk: docker
app_file: app.py
pinned: false
---

# Local Food Analysis API

A FastAPI-based inference service for local food regression and clustering analysis. This Space provides ML model predictions for XGBoost regression and KMeans clustering.

## Features

- **🎯 Regression Prediction**: XGBoost model for food analysis predictions
- **🗂️ Clustering**: KMeans clustering with probability scores
- **🗺️ Map Data**: Pre-computed clustering results for visualization
- **⚡ Fast Inference**: Optimized model loading and prediction pipeline
- **📊 Scalable**: Feature scaling with joblib-saved scalers

## API Endpoints

### POST `/predict`
Make a regression prediction.

**Request:**
```json
{
  "features": {
    "feature_1": 5.2,
    "feature_2": 10,
    "feature_3": "category_value"
  }
}
```

**Response:**
```json
{
  "prediction": 42.5,
  "confidence": 0.85,
  "model_used": "XGBoost Regressor"
}
```

### POST `/cluster`
Assign a cluster for given features.

**Request:**
```json
{
  "features": {
    "feature_1": 5.2,
    "feature_2": 10
  }
}
```

**Response:**
```json
{
  "cluster": 1,
  "probability": 0.92,
  "coordinates": {
    "x": 0.5,
    "y": 0.3
  }
}
```

### GET `/clustering-map`
Get all clustering data for map visualization.

**Response:**
```json
{
  "clusters": {
    "0": {
      "name": "Cluster 0",
      "centroid": {"x": 0.5, "y": 0.5},
      "color": "#FF6B6B",
      "counties": []
    }
  }
}
```

### GET `/health`
Health check endpoint.

**Response:**
```json
{
  "status": "ok",
  "models": {
    "regression": true,
    "clustering": true
  }
}
```

## Model Files

This Space expects the following files in the root directory:

- `xgboost_tuned_model.joblib` - Trained XGBoost regression model
- `kmeans_model.pkl` - Trained KMeans clustering model
- `scaler_regression.pkl` - StandardScaler for regression features
- `scaler.pkl` - StandardScaler for clustering features
- `scaled_columns.pkl` - List of column names for feature scaling
- `clustering_features.json` - Feature configuration and metadata
- `clustering_map_data.json` - Pre-computed clustering results (optional)

## Configuration

Edit `clustering_features.json` to describe your features:

```json
{
  "feature_name": {
    "display_name": "Feature Display Name",
    "description": "Feature description",
    "type": "numeric|categorical",
    "min": 0,
    "max": 100,
    "categories": ["cat1", "cat2"]
  }
}
```

## Deployment

1. Create a Space on Hugging Face
2. Select Docker runtime
3. Push files or use `upload_models.py`
4. Configure Space settings:
   - Dockerfile should be at root
   - Exposed port: 7860
5. Space will auto-build and deploy

## Environment Variables

Optional environment variables:

- `PORT` - Server port (default: 7860)
- `DEBUG` - Enable debug logging (default: false)

## Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn app:app --host 0.0.0.0 --port 7860 --reload

# Test endpoint
curl -X POST http://localhost:7860/predict \
  -H "Content-Type: application/json" \
  -d '{"features": {"feature_1": 5.2}}'
```

## Docker Build

```bash
docker build -t local-food-api .
docker run -p 7860:7860 local-food-api
```

## Troubleshooting

### Models not loading
- Check file paths in `app.py`
- Ensure all `.joblib` and `.pkl` files are in root
- Check Space logs for error details

### Feature scaling issues
- Verify `scaled_columns.pkl` contains correct feature order
- Ensure input features match training feature names

### Slow inference
- Models are loaded once at startup
- First request may take longer due to model initialization
- Check Space resources and consider upgrading

## Performance

Typical response times:
- Regression prediction: ~50-100ms
- Clustering: ~30-50ms
- Map data retrieval: ~20-30ms

## Support

For issues or questions, create a Space discussion or commit to the repository.

## License

This code is part of the US FoodScope project.
