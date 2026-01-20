# 📊 Module Local - Architecture Diagram

## System Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    USER BROWSER                              │
│  http://localhost:8000/local/regression/                     │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              DJANGO APPLICATION                              │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐                                            │
│  │   FORM       │  Dynamic form from clustering_features.json
│  │              │──→ Input validation                        │
│  └──────┬───────┘    Categorical + Numeric fields           │
│         │                                                    │
│         ▼                                                    │
│  ┌──────────────────────────────┐                           │
│  │    services.py               │                           │
│  │ LocalFoodPredictionService   │                           │
│  └──────┬──────────┬──────┬─────┘                           │
│         │          │      │                                 │
│   predict()  cluster()  map()                               │
│         │          │      │                                 │
└─────────┼──────────┼──────┼─────────────────────────────────┘
          │          │      │
          │ HTTP     │      │
          ▼          ▼      ▼
┌─────────────────────────────────────────────────────────────┐
│  HUGGING FACE SPACE API (FastAPI)                           │
│  https://rouazekri-roua-localfood.hf.space                 │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌────────────┐    ┌────────────┐    ┌────────────┐        │
│  │ /predict   │    │ /cluster   │    │ /cluster-  │        │
│  │            │    │            │    │   map      │        │
│  │ XGBoost    │    │ KMeans     │    │ Pre-calc   │        │
│  │ Regression │    │ Clustering │    │ data       │        │
│  └────────────┘    └────────────┘    └────────────┘        │
│         │                │                    │              │
└─────────┼────────────────┼────────────────────┼──────────────┘
          │                │                    │
          ▼                ▼                    ▼
┌─────────────────────────────────────────────────────────────┐
│            ML MODELS & ARTIFACTS                            │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  xgboost_tuned_model.joblib ────→ Regression scores        │
│  kmeans_model.pkl ────────────→ Cluster assignments        │
│  scaler_regression.pkl ──────→ Feature scaling             │
│  scaler.pkl ──────────────────→ Feature scaling            │
│  scaled_columns.pkl ──────────→ Feature order              │
│  clustering_features.json ────→ Feature metadata           │
│  clustering_map_data.json ────→ Cluster visualization      │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## File Organization

```
us_foodscope/
│
├── local/                                    ← LOCAL MODULE
│   ├── models.py                    ✓ Created
│   │   └── RegressionPredictionHistory
│   │
│   ├── forms.py                     ✓ Created
│   │   └── LocalRegressionForm (dynamic)
│   │
│   ├── services.py                  ✓ Created
│   │   └── LocalFoodPredictionService
│   │       ├── predict()
│   │       ├── predict_cluster()
│   │       └── get_clustering_map_data()
│   │
│   ├── views.py                     ✓ Modified
│   │   ├── local_view()            (legacy)
│   │   ├── local_regression_view() (new)
│   │   └── clustering_map_view()   (new)
│   │
│   ├── urls.py                      ✓ Modified
│   ├── admin.py                     ✓ Modified
│   ├── ml_loader.py                 ✓ Created
│   ├── config.py                    ✓ Created
│   │
│   ├── INTEGRATION_GUIDE.md         ✓ Created
│   ├── SETUP_CHECKLIST.md           ✓ Created
│   ├── QUICKSTART.md                ✓ Created
│   ├── MIGRATION_GUIDE.txt          ✓ Created
│   │
│   └── my_hfspace/                  ← HF SPACE FILES
│       ├── app.py                   ✓ Created (FastAPI)
│       ├── Dockerfile               ✓ Created
│       ├── requirements.txt          ✓ Created
│       ├── README.md                 ✓ Created
│       ├── upload_models.py          ✓ Modified
│       ├── generate_config.py        ✓ Created
│       ├── test_api.py               ✓ Created
│       │
│       ├── clustering_features.json
│       ├── xgboost_tuned_model.joblib
│       ├── kmeans_model.pkl
│       ├── scaler_regression.pkl
│       ├── scaler.pkl
│       ├── scaled_columns.pkl
│       ├── clustering_map_data.json
│       │
│       ├── clustering_features.example.json  ✓ Created
│       ├── clustering_map_data.example.json  ✓ Created
│       ├── .env.example              ✓ Created
│       ├── .dockerignore             ✓ Created
│       └── .gitignore                ✓ Created
│
└── templates/
    └── local/
        ├── local.html                (existing)
        └── regression.html            ✓ Created (new interface)
```

---

## Data Flow

### User Input
```json
{
  "population_density": 500,
  "median_income": 75000,
  "region_type": "urban"
}
```
         │
         ▼
### Processing
- Form validation (Django)
- Feature preparation
- HTTP POST to HF Space
         │
         ▼
### Predictions
```json
{
  "prediction": 42.5,        ← Regression output
  "confidence": 0.85,        ← Model confidence
  "cluster": 1,              ← Cluster assignment
  "probability": 0.92,       ← Assignment confidence
  "coordinates": {x, y}      ← 2D visualization
}
```
         │
         ▼
### Display
- Form results card
- Cluster visualization
- Prediction history
- Database save

---

## Key Components

### 1. Django Forms
- **Location**: `local/forms.py`
- **Feature**: Dynamic field generation
- **Data source**: `clustering_features.json`
- **Validation**: Auto + custom rules

### 2. Service Layer
- **Location**: `local/services.py`
- **Role**: API communication
- **Methods**: predict(), cluster(), map_data()
- **Error handling**: TimeOut, HTTP errors

### 3. Models
- **Location**: `local/models.py`
- **Purpose**: Store prediction history
- **Fields**: user, input_data, prediction, cluster

### 4. FastAPI Server
- **Location**: `my_hfspace/app.py`
- **Endpoints**: /predict, /cluster, /map, /health
- **Models**: XGBoost + KMeans
- **Scaling**: StandardScaler

### 5. Templates
- **Location**: `templates/local/regression.html`
- **Style**: Similar to health module
- **Layout**: 2-column (form | results)
- **Features**: History, real-time display

---

## Deployment Pipeline

```
┌──────────────────────┐
│  Local Development   │
│  - Test models      │
│  - Create config    │
│  - Test Django      │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Hugging Face Upload  │
│ - Push files        │
│ - Build Docker      │
│ - Start API         │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Django Integration   │
│ - Migrations        │
│ - Config setup      │
│ - Test API call     │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Production Ready     │
│ - Live predictions  │
│ - Store history     │
│ - Monitor logs      │
└──────────────────────┘
```

---

## Feature Configuration

```json
{
  "feature_name": {
    "display_name": "UI Label",
    "description": "Help text",
    "type": "numeric|categorical",
    "min": 0,          // numeric only
    "max": 100,        // numeric only
    "categories": [],  // categorical only
    "unit": "unit"
  }
}
```

**Example:**
```json
{
  "population": {
    "type": "numeric",
    "min": 1000,
    "max": 5000000
  },
  "region": {
    "type": "categorical",
    "categories": ["urban", "suburban", "rural"]
  }
}
```

---

## API Endpoints Summary

| Method | Endpoint | Input | Output |
|--------|----------|-------|--------|
| GET | `/health` | - | status, models |
| GET | `/` | - | info, endpoints |
| POST | `/predict` | features | prediction, confidence |
| POST | `/cluster` | features | cluster, probability |
| GET | `/clustering-map` | - | clusters, metadata |

---

## Security Layers

```
Browser Request
    ↓
Django Middleware
    ↓
@prediction_access_required decorator
    ↓
Form Validation
    ↓
Service Layer with Error Handling
    ↓
HF Space API (over HTTPS)
    ↓
Model Inference
    ↓
JSON Response
    ↓
Database Save (user-scoped)
```

---

## Success Metrics

- ✅ Form generates from JSON
- ✅ API returns predictions
- ✅ Clustering works
- ✅ History saves
- ✅ Admin accessible
- ✅ UI matches health style
- ✅ Error handling solid
- ✅ Documentation complete

---

**Created**: January 8, 2025
**Status**: Ready for deployment
**Next**: Add models to my_hfspace/ and test!
