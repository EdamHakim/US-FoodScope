# 🍔 Local Food Module - Complete Implementation

> Régression + Clustering for Local Food Analysis with Hugging Face Integration

## 📋 Overview

This module provides a complete end-to-end solution for:
- **Regression Prediction**: XGBoost model predictions
- **Clustering Analysis**: KMeans cluster assignments
- **Map Visualization**: Interactive cluster visualization
- **History Tracking**: Persistent prediction storage

## ⚡ Quick Links

- 📖 [Quick Start (5 min)](QUICKSTART.md)
- 🔧 [Integration Guide (Detailed)](INTEGRATION_GUIDE.md)
- ✅ [Setup Checklist](SETUP_CHECKLIST.md)
- 🏗️ [Architecture Diagram](ARCHITECTURE.md)
- 🚀 [Deployment Instructions](my_hfspace/README.md)

## 🎯 Features

✅ **Dynamic Form Generation**
- Features loaded from `clustering_features.json`
- Automatic validation
- Numeric and categorical support

✅ **Remote Inference**
- XGBoost regression via FastAPI
- KMeans clustering via HF Space
- Error handling & timeouts

✅ **User Interface**
- 2-column layout (form + results)
- Real-time results display
- Prediction history
- Responsive design

✅ **Data Persistence**
- Django model for history
- User-scoped predictions
- Admin interface

✅ **Production Ready**
- Docker containerization
- Health checks
- Comprehensive logging
- Test suite included

## 📁 File Structure

```
local/
├── Core Django Files
│   ├── models.py              # Prediction history model
│   ├── forms.py               # Dynamic form
│   ├── views.py               # Request handlers
│   ├── urls.py                # URL routing
│   ├── admin.py               # Admin interface
│   ├── services.py            # HF Space API client
│   ├── ml_loader.py           # Feature loader
│   └── config.py              # Configuration
│
├── Templates
│   └── regression.html        # Main interface
│
├── HF Space Files (my_hfspace/)
│   ├── app.py                 # FastAPI server
│   ├── Dockerfile             # Container config
│   ├── requirements.txt        # Python packages
│   ├── upload_models.py       # Deployment script
│   ├── generate_config.py     # Config generator
│   ├── test_api.py            # Test suite
│   ├── README.md              # API docs
│   ├── clustering_features.json
│   ├── xgboost_tuned_model.joblib
│   ├── kmeans_model.pkl
│   ├── scaler_regression.pkl
│   ├── scaler.pkl
│   └── scaled_columns.pkl
│
└── Documentation
    ├── QUICKSTART.md
    ├── INTEGRATION_GUIDE.md
    ├── SETUP_CHECKLIST.md
    ├── ARCHITECTURE.md
    ├── MIGRATION_GUIDE.txt
    └── FILES_SUMMARY.json
```

## 🚀 Quick Start

### 1. Prepare Models

Copy your trained models to `my_hfspace/`:
```bash
cp xgboost_tuned_model.joblib local/my_hfspace/
cp kmeans_model.pkl local/my_hfspace/
cp scaler_regression.pkl local/my_hfspace/
cp scaler.pkl local/my_hfspace/
cp scaled_columns.pkl local/my_hfspace/
```

### 2. Configure Features

Edit `my_hfspace/clustering_features.json`:
```json
{
  "population": {"type": "numeric", "min": 0, "max": 5000000},
  "income": {"type": "numeric", "min": 20000, "max": 200000}
}
```

### 3. Deploy to HF

```bash
cd my_hfspace
pip install huggingface_hub
python upload_models.py
```

### 4. Setup Django

```bash
python manage.py makemigrations local
python manage.py migrate local
python manage.py runserver
```

### 5. Test

```bash
# Test API
python local/my_hfspace/test_api.py

# Access interface
# http://localhost:8000/local/regression/
```

## 🎨 UI Preview

```
┌─────────────────────────────────┬──────────────────────────────┐
│   INPUT FORM                    │   RESULTS                    │
│                                 │                              │
│  □ Population Density           │  ✓ Prediction: 42.5         │
│  □ Median Income                │                              │
│  □ Poverty Rate                 │  📊 Cluster: #1 (92%)       │
│  □ Region Type                  │                              │
│                                 │  🗺️ Map Data                │
│  [Predict & Cluster] [Clear]    │                              │
│                                 │  📜 Recent Predictions       │
│  📜 History                      │                              │
│  • Jan 8, 12:30                 │                              │
│  • Jan 8, 12:15                 │                              │
└─────────────────────────────────┴──────────────────────────────┘
```

## 🔧 Configuration

### Django Settings

```python
INSTALLED_APPS = ['local', ...]

LOCAL_FOOD_HF_API_URL = "https://rouazekri-roua-localfood.hf.space"
```

### Feature Definition

```json
{
  "feature_name": {
    "display_name": "UI Label",
    "type": "numeric|categorical",
    "min": 0,
    "max": 100,
    "categories": ["a", "b", "c"]  // categorical only
  }
}
```

## 📊 API Endpoints

### Django Routes
```
GET  /local/regression/           - Prediction interface
GET  /local/api/clustering-map/   - Map data API
```

### HF Space API
```
GET  /health                      - Health check
POST /predict                     - Regression
POST /cluster                     - Clustering
GET  /clustering-map              - Map data
```

## 🧪 Testing

### Unit Tests
```bash
python manage.py test local
```

### API Tests
```bash
python local/my_hfspace/test_api.py
```

### Manual Testing
1. Navigate to `http://localhost:8000/local/regression/`
2. Fill the form
3. Click "Predict & Cluster"
4. Verify results display
5. Check database for history

## 🔐 Security

- ✅ Form validation
- ✅ Access control via decorators
- ✅ Error handling
- ✅ HTTPS API communication
- ✅ User-scoped data
- ✅ No credential exposure

## 📈 Performance

Expected response times:
- Form load: < 100ms
- Regression prediction: 50-100ms
- Clustering: 30-50ms
- Total: < 200ms

## 🐛 Troubleshooting

### API not responding
```bash
curl https://rouazekri-roua-localfood.hf.space/health
```

### Form not showing fields
- Check `clustering_features.json` exists
- Validate JSON syntax
- Check feature names match

### Predictions incorrect
- Verify feature order in `scaled_columns.pkl`
- Check min/max ranges
- Verify model files present

### Database errors
- Run migrations: `python manage.py migrate local`
- Check user permissions
- Review Django logs

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| [QUICKSTART.md](QUICKSTART.md) | 5-minute setup |
| [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md) | Complete guide |
| [SETUP_CHECKLIST.md](SETUP_CHECKLIST.md) | Deployment checklist |
| [ARCHITECTURE.md](ARCHITECTURE.md) | System design |
| [my_hfspace/README.md](my_hfspace/README.md) | API documentation |

## 🎓 Learn More

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Django Documentation](https://docs.djangoproject.com/)
- [Hugging Face Spaces](https://huggingface.co/spaces)
- [XGBoost Guide](https://xgboost.readthedocs.io/)
- [Scikit-learn](https://scikit-learn.org/)

## ✨ Key Highlights

- **Zero Model Management**: Models live on HF Space, not in Django
- **Dynamic Forms**: Features loaded from JSON, no hardcoding
- **Automatic Scaling**: Feature preparation handled by HF API
- **History Tracking**: All predictions saved with user context
- **Admin Interface**: Manage predictions in Django admin
- **Responsive Design**: Works on mobile and desktop
- **Error Resilience**: Comprehensive error handling
- **Documented**: Complete docs and examples

## 📝 Customization Examples

### Add Custom Validation
```python
# forms.py
class LocalRegressionForm(forms.Form):
    def clean_population(self):
        value = self.cleaned_data.get('population')
        if value > 5000000:
            raise ValidationError("Too high")
        return value
```

### Change Styling
Edit `templates/local/regression.html`:
```html
<style>
  .submit-btn {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  }
</style>
```

### Add Custom Processing
```python
# views.py
if request.method == 'POST':
    # ... form processing
    
    # Custom logic
    result = my_custom_function(prediction_result)
    
    context['custom_data'] = result
```

## 🤝 Contributing

To extend this module:
1. Follow Django best practices
2. Update documentation
3. Add tests for new features
4. Test locally before deployment

## 📧 Support

For issues:
1. Check troubleshooting guide
2. Review relevant documentation
3. Check HF Space logs
4. Review Django debug output

## 📄 License

Part of US FoodScope Project

---

**Status**: ✅ Ready for deployment  
**Last Updated**: January 8, 2025  
**Version**: 1.0

🎉 **Ready to predict?** Start with [QUICKSTART.md](QUICKSTART.md)!
