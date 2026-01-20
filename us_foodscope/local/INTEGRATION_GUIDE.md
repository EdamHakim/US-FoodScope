# Guide d'Intégration - Module Local Food

## 📋 Vue d'ensemble

Ce guide explique comment intégrer complètement le module `local` avec vos modèles XGBoost et KMeans hébergés sur Hugging Face.

## 🎯 Architecture

```
Django Application (local/)
    ↓
    Service Layer (services.py)
    ↓
    Hugging Face Space API (https://rouazekri-roua-localfood.hf.space)
    ↓
    Models (xgboost_tuned_model.joblib, kmeans_model.pkl)
```

## 📂 Structure des fichiers

### Django Module (`us_foodscope/local/`)

```
local/
├── __init__.py
├── admin.py
├── apps.py
├── config.py                    # Configuration module
├── forms.py                     # Django form for input
├── ml_loader.py                # Feature configuration loader
├── models.py                   # Django models (RegressionPredictionHistory)
├── services.py                 # HF Space API client
├── urls.py                     # URL routing
├── views.py                    # View handlers
├── my_hfspace/
│   ├── app.py                 # FastAPI inference server
│   ├── Dockerfile             # Docker container definition
│   ├── requirements.txt        # Python dependencies
│   ├── README.md              # API documentation
│   ├── upload_models.py       # Deployment script
│   ├── generate_config.py     # Config generator
│   ├── clustering_features.json
│   ├── xgboost_tuned_model.joblib
│   ├── kmeans_model.pkl
│   ├── scaler_regression.pkl
│   ├── scaler.pkl
│   ├── scaled_columns.pkl
│   └── clustering_map_data.json (optional)
└── migrations/
```

### Templates (`us_foodscope/templates/local/`)

```
local/
├── regression.html             # Main prediction interface
└── local.html                 # Legacy home page
```

## 🚀 Étapes d'installation

### 1. Mettre à jour `settings.py`

```python
INSTALLED_APPS = [
    # ... autres apps
    'local',
]

# Configuration du module local
LOCAL_FOOD_HF_API_URL = "https://rouazekri-roua-localfood.hf.space"

# Logging (optionnel)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'local.services': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    },
}
```

### 2. Configurer le fichier `clustering_features.json`

Ce fichier décrit vos features de clustering pour le formulaire dynamique.

**Exemple:**

```json
{
  "population_density": {
    "display_name": "Population Density",
    "description": "Number of people per square mile",
    "type": "numeric",
    "min": 0,
    "max": 10000,
    "unit": "people/sq mile"
  },
  "median_income": {
    "display_name": "Median Income",
    "description": "Median household income in dollars",
    "type": "numeric",
    "min": 20000,
    "max": 200000,
    "unit": "USD"
  },
  "region_type": {
    "display_name": "Region Type",
    "description": "Type of geographic region",
    "type": "categorical",
    "categories": ["urban", "suburban", "rural"]
  }
}
```

### 3. Préparer vos modèles

**Location:** `local/my_hfspace/`

Vos fichiers de modèles doivent être présents:

```bash
cd local/my_hfspace
ls -la
```

**Fichiers requis:**
- `xgboost_tuned_model.joblib` - XGBoost regression model
- `kmeans_model.pkl` - KMeans clustering model
- `scaler_regression.pkl` - StandardScaler for regression features
- `scaler.pkl` - StandardScaler for clustering features
- `scaled_columns.pkl` - Feature order list

### 4. Déployer sur Hugging Face

#### Option A: Via script Python

```bash
cd local/my_hfspace

# Installer dépendances de déploiement
pip install huggingface_hub

# Mettre à jour vos credentials dans upload_models.py
# - HF_SPACE_NAME = "rouazekri-roua-localfood"
# - HF_USERNAME = "rouazekri"

# Exécuter le upload
python upload_models.py
```

#### Option B: Via Git (recommandé pour Hugging Face)

```bash
# Cloner votre space
git clone https://huggingface.co/spaces/rouazekri/rouazekri-roua-localfood
cd rouazekri-roua-localfood

# Copier les fichiers de local/my_hfspace
cp local/my_hfspace/* .

# Committer et pusher
git add -A
git commit -m "Deploy local food models"
git push
```

### 5. Configurer les migrations Django

```bash
# Créer les migrations pour le nouveau modèle
python manage.py makemigrations local

# Appliquer les migrations
python manage.py migrate local
```

## 🔧 Configuration des variables d'environnement

**Fichier `.env` (à la racine du projet):**

```
# Hugging Face Configuration
LOCAL_FOOD_HF_API_URL=https://rouazekri-roua-localfood.hf.space

# Django Debug
DEBUG=False

# Database
DATABASE_URL=sqlite:///db.sqlite3
```

## 📡 Vérifier l'intégration

### 1. Vérifier l'API HF

```bash
# Health check
curl https://rouazekri-roua-localfood.hf.space/health

# Expected response:
# {
#   "status": "ok",
#   "models": {
#     "regression": true,
#     "clustering": true
#   }
# }
```

### 2. Tester localement

```bash
# Démarrer le serveur Django
python manage.py runserver

# Accéder à http://localhost:8000/local/regression/
```

### 3. Logs de diagnostic

```python
# Dans views.py ou services.py
import logging
logger = logging.getLogger(__name__)
logger.info(f"Calling HF API: {endpoint}")
```

## 🎨 Personnaliser l'interface

### Modifier le formulaire

**Fichier:** `local/forms.py`

Le formulaire est généré dynamiquement à partir de `clustering_features.json`. Pour ajouter des validations personnalisées:

```python
class LocalRegressionForm(forms.Form):
    def clean_population_density(self):
        value = self.cleaned_data.get('population_density')
        if value and value > 10000:
            raise forms.ValidationError("Population density cannot exceed 10,000")
        return value
```

### Modifier le template

**Fichier:** `templates/local/regression.html`

Le template utilise un système de grille CSS flexible. Pour personnaliser le style:

```html
<!-- Modifier la section result-metric -->
<div class="result-metric">
    <!-- Votre code personnalisé -->
</div>
```

## 📊 Gérer l'historique des prédictions

Les prédictions sont automatiquement sauvegardées dans la base de données Django.

```python
# Accéder à l'historique
from local.models import RegressionPredictionHistory

# Pour un utilisateur spécifique
user_predictions = RegressionPredictionHistory.objects.filter(
    user=request.user
).order_by('-created_at')

# Pour une prédiction spécifique
prediction = RegressionPredictionHistory.objects.get(id=123)
print(prediction.prediction_value)
print(prediction.cluster_assigned)
print(prediction.input_data)
```

## 🐛 Dépannage

### L'API HF n'est pas accessible

```bash
# Vérifier la santé de l'API
curl -I https://rouazekri-roua-localfood.hf.space/health

# Si erreur 503: Le Space est peut-être en construction
# Vérifier les logs du Space sur Hugging Face
```

### Les modèles ne se chargent pas

**Message d'erreur:** "Regression model not loaded"

**Solution:**
1. Vérifier que `xgboost_tuned_model.joblib` existe dans le Space
2. Vérifier les logs du Space
3. Re-uploader les fichiers

### Les features n'apparaissent pas dans le formulaire

**Vérifier:**
1. `clustering_features.json` existe dans `local/my_hfspace/`
2. Le JSON est valide (tester avec `json.loads()`)
3. Les noms de features correspondent à vos modèles

### Problèmes de scaling

**Si les prédictions sont incorrectes:**
1. Vérifier que `scaled_columns.pkl` contient le bon ordre des features
2. Vérifier que `scaler_regression.pkl` et `scaler.pkl` sont les bons scalers
3. Vérifier les ranges min/max dans `clustering_features.json`

## 📝 Exemple d'utilisation complète

```python
# 1. Accéder à la page de prédiction
# http://localhost:8000/local/regression/

# 2. Remplir le formulaire avec les données
# (formulaire généré dynamiquement à partir de clustering_features.json)

# 3. Cliquer "Predict & Cluster"

# 4. Résultats affichés:
# - Valeur de prédiction (régression)
# - Cluster assigné (clustering)
# - Carte de visualisation

# 5. L'historique est sauvegardé en base de données
# Accessible via:
# from local.models import RegressionPredictionHistory
# RegressionPredictionHistory.objects.filter(user=request.user)
```

## 🔐 Sécurité

- ✅ Validation des formulaires Django
- ✅ Décorateur `@prediction_access_required` pour contrôler l'accès
- ✅ Timeout sur les requêtes API (10 secondes)
- ✅ Gestion des erreurs API
- ✅ Logging des activités

## 🚀 Optimisations futures

- [ ] Caching des résultats clustering
- [ ] Support du déploiement multi-région
- [ ] API GraphQL alternative
- [ ] WebSocket pour streaming des résultats
- [ ] Sauvegarde d'exports (PDF, CSV)

## 📧 Support

Pour les problèmes ou questions:
1. Vérifier les logs du Space HF
2. Consulter la documentation FastAPI: http://rouazekri-roua-localfood.hf.space/docs
3. Vérifier les migrations Django: `python manage.py showmigrations`

## ✅ Checklist de déploiement

- [ ] Fichiers modèles présents dans `local/my_hfspace/`
- [ ] `clustering_features.json` configuré correctement
- [ ] Dockerfile et requirements.txt à jour
- [ ] Fichiers uploadés sur HF Space
- [ ] API HF fonctionnelle (test health check)
- [ ] Django migrations appliquées
- [ ] `settings.py` configuré avec `LOCAL_FOOD_HF_API_URL`
- [ ] Templates testés sur localhost
- [ ] Formulaire affiche toutes les features
- [ ] Prédictions retournées correctement
