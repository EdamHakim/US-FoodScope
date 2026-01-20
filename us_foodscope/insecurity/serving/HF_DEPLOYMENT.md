# Hugging Face Spaces Deployment Guide

## Step-by-Step Deployment Instructions

### 1. Create a Hugging Face Space

1. Go to [huggingface.co/spaces](https://huggingface.co/spaces)
2. Click "Create new Space"
3. Fill in the form:
   - **Space name**: `us-food-insecurity-prediction` (or your preferred name)
   - **License**: Choose appropriate license (MIT, Apache-2.0, etc.)
   - **Space SDK**: Select **Docker**
   - **Visibility**: Public (to share with professor) or Private
4. Click "Create Space"

### 2. Connect Your Local Repository

```bash
# Navigate to your insecurity/serving directory
cd path/to/US_FoodScope/us_foodscope/insecurity/serving

# Clone your Space repo
git clone https://huggingface.co/spaces/<your-username>/<space-name>
cd <space-name>
```

### 3. Copy Files to Space

Copy all files from `insecurity/serving/` to your cloned Space directory:

```bash
# Option A: Manual copy
cp /path/to/insecurity/serving/* .

# Option B: PowerShell (Windows)
Copy-Item -Path "C:\path\to\insecurity\serving\*" -Destination "." -Recurse -Force
```

**Files to include**:
- `app.py`
- `Dockerfile`
- `requirement.txt` (note: file is named `requirement.txt` not `requirements.txt`)
- `rf_foodinsecurity_predictor.pkl`
- `kmeans_food_access.pkl`
- `scaler_foodinsecurity.pkl`
- `scaler_food_access.pkl`
- `model_metadata.json`
- `county_clusters.csv`
- `README.md`
- `.gitignore`

### 4. Push to Hugging Face

```bash
# Navigate to Space directory
cd <space-name>

# Configure git (if needed)
git config user.email "your-email@example.com"
git config user.name "Your Name"

# Add all files
git add .

# Commit
git commit -m "Add US Food Insecurity Prediction API"

# Push to Hugging Face
git push
```

### 5. Monitor Deployment

1. Go to your Space URL: `https://huggingface.co/spaces/<username>/<space-name>`
2. Watch the "Logs" tab for build progress
3. Once built, your API will be live!

## Testing Your Deployed API

### Using the Interactive API Docs

Once deployed, access the interactive API documentation:
```
https://huggingface.co/spaces/<username>/<space-name>
```

The Space will automatically create an interface with:
- `/docs` - Swagger UI for testing endpoints
- `/redoc` - ReDoc documentation
- All endpoints ready to test

### Testing with curl (from command line)

```bash
# Test health check
curl https://<username>-<space-name>.hf.space/

# Get clustering data
curl https://<username>-<space-name>.hf.space/clustering-data

# Make a prediction
curl -X POST https://<username>-<space-name>.hf.space/predict \
  -H "Content-Type: application/json" \
  -d '{
    "PCT_LACCESS_POP15": 5.2,
    "LACCESS_BLACK15": 3.1,
    "LACCESS_HISP15": 4.8,
    "LACCESS_NHASIAN15": 2.5,
    "Poverty_Rate": 15.3,
    "Adult_Obesity_Rate13": 28.5,
    "Adult_Diabetes_Rate13": 9.2,
    "FOODINSEC_13_15": 12.4
  }'

# Get model info
curl https://<username>-<space-name>.hf.space/model-info
```

### Testing with Python

```python
import requests

BASE_URL = "https://<username>-<space-name>.hf.space"

# Health check
response = requests.get(f"{BASE_URL}/")
print(response.json())

# Make prediction
prediction_data = {
    "PCT_LACCESS_POP15": 5.2,
    "LACCESS_BLACK15": 3.1,
    "LACCESS_HISP15": 4.8,
    "LACCESS_NHASIAN15": 2.5,
    "Poverty_Rate": 15.3,
    "Adult_Obesity_Rate13": 28.5,
    "Adult_Diabetes_Rate13": 9.2,
    "FOODINSEC_13_15": 12.4
}

response = requests.post(f"{BASE_URL}/predict", json=prediction_data)
print(response.json())
```

## Understanding the File Structure

```
insecurity/serving/
├── app.py                           # FastAPI application (main code)
├── Dockerfile                       # Docker container configuration
├── requirement.txt                  # Python dependencies
├── README.md                        # Documentation
├── .gitignore                       # Git ignore rules
│
├── rf_foodinsecurity_predictor.pkl  # Random Forest model (160 MB)
├── kmeans_food_access.pkl           # KMeans clustering model
├── scaler_foodinsecurity.pkl        # Feature scaler for predictions
├── scaler_food_access.pkl           # Feature scaler for clustering
├── model_metadata.json              # Model configuration
└── county_clusters.csv              # Pre-computed clustering results
```

## API Endpoints Reference

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | Health check |
| `/clustering-data` | GET | Get all county clustering data |
| `/predict` | POST | Predict food insecurity |
| `/model-info` | GET | Get model metadata |
| `/docs` | GET | Interactive API documentation |
| `/openapi.json` | GET | OpenAPI schema |

## Troubleshooting

### Build fails with "File not found"

**Problem**: Dockerfile or app.py can't be found
- **Solution**: Make sure files are in the Space directory root, not in subdirectories

### Models fail to load

**Problem**: `ModuleNotFoundError` or model files missing
- **Solution**: Verify all `.pkl` and `.json` files are in the Space directory

### Memory issues

**Problem**: Space runs out of memory during build/runtime
- **Solution**: Hugging Face Spaces provide 16GB RAM - if still failing, check model file sizes

### Large file size

**Problem**: Git push fails because files are too large
- **Solution**: Use [Git LFS](https://huggingface.co/docs/hub/repositories-tips-and-tricks#using-git-lfs):
  ```bash
  git lfs install
  git lfs track "*.pkl"
  git lfs track "*.joblib"
  git add .gitattributes
  ```

## Integration with Django App

You can call your deployed API from your Django application:

```python
# In your Django views
import requests

def get_prediction(features_dict):
    url = "https://<username>-<space-name>.hf.space/predict"
    response = requests.post(url, json=features_dict)
    return response.json()
```

## Sharing with Professor

1. **Share the Space URL**: `https://huggingface.co/spaces/<username>/<space-name>`
2. **Share this README**: Include link to the documentation
3. **Mention the features**:
   - Interactive API documentation
   - Real-time prediction capability
   - Clustering analysis of ~3,100 US counties
   - Professional inference server

## Next Steps

After successful deployment:

1. ✅ Test all endpoints with sample data
2. ✅ Share Space URL with professor
3. ✅ Create a presentation showing the model performance
4. ✅ Consider adding a simple web UI using Gradio for easier interaction (optional)

---

**Need help?** Refer to [Hugging Face Spaces Documentation](https://huggingface.co/docs/hub/spaces)
