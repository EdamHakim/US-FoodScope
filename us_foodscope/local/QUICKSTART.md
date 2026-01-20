# 🚀 Quick Start Guide - Local Food Module

## ⚡ 5 minutes setup

### 1️⃣ Préparer vos modèles

Copier dans `local/my_hfspace/`:
```
xgboost_tuned_model.joblib
kmeans_model.pkl
scaler_regression.pkl
scaler.pkl
scaled_columns.pkl
```

### 2️⃣ Configurer les features

Éditer `local/my_hfspace/clustering_features.json`:

```json
{
  "votre_feature_1": {
    "display_name": "Nom Affichable",
    "type": "numeric",
    "min": 0,
    "max": 100
  }
}
```

⚠️ **Important**: Les noms doivent correspondre exactement à vos données d'entraînement!

### 3️⃣ Déployer sur HF

```bash
cd local/my_hfspace

pip install huggingface_hub
python upload_models.py
```

Ou avec Git:
```bash
git clone https://huggingface.co/spaces/rouazekri/rouazekri-roua-localfood
cp local/my_hfspace/* .
git add -A && git commit -m "Deploy" && git push
```

### 4️⃣ Migrer Django

```bash
python manage.py makemigrations local
python manage.py migrate local
```

### 5️⃣ Tester

```bash
# Test API HF
python local/my_hfspace/test_api.py

# Test Django
python manage.py runserver
# Visiter: http://localhost:8000/local/regression/
```

---

## 📋 Fichiers clés à personnaliser

1. **`local/my_hfspace/clustering_features.json`**
   - Ajouter/modifier vos features
   - Mettre à jour min/max

2. **`local/my_hfspace/app.py`**
   - Lignes 19-22: Vérifier paths des modèles
   - Fonction `prepare_features_for_model()`: adapter si besoin

3. **`settings.py` (Django)**
   - Ajouter: `LOCAL_FOOD_HF_API_URL = "..."`

---

## 🧪 Tests rapides

```bash
# Vérifier API
curl https://rouazekri-roua-localfood.hf.space/health

# Test localement
curl -X POST http://localhost:7860/predict \
  -H "Content-Type: application/json" \
  -d '{"features": {"your_feature": 5.2}}'
```

---

## 🎨 Le formulaire se génère automatiquement

À partir de `clustering_features.json`:
- Les champs sont créés dynamiquement
- Les validations s'appliquent automatiquement
- Le style est cohérent avec health module

---

## 🗺️ Ajouter une Map

Template prêt pour Leaflet/Mapbox:

```html
<div id="clustering-map" style="height: 400px;"></div>

<script>
const map = L.map('clustering-map').setView([center], zoom);
// Ajouter clusters...
</script>
```

---

## 🔧 Troubleshooting

| Problème | Solution |
|----------|----------|
| Formulaire vide | Vérifier `clustering_features.json` |
| API timeout | Vérifier l'URL HF |
| Models not found | Vérifier paths dans `app.py` |
| Import errors | Vérifier `requirements.txt` |

---

## 📝 Exemple complet

**clustering_features.json:**
```json
{
  "population": {"type": "numeric", "min": 1000, "max": 5000000},
  "income": {"type": "numeric", "min": 20000, "max": 200000},
  "region": {"type": "categorical", "categories": ["urban", "rural"]}
}
```

**Test request:**
```bash
curl -X POST https://api.hf.space/predict \
  -d '{"features": {"population": 500000, "income": 75000, "region": "urban"}}'
```

---

## ✅ Success criteria

- [ ] API HF répond au health check
- [ ] Formulaire affiche tous les champs
- [ ] Prédiction retourne un nombre
- [ ] Cluster retourne un entier
- [ ] Historique sauvegardé en DB
- [ ] Interface affiche les résultats

---

## 📚 Docs complètes

- [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md) - Guide complet
- [SETUP_CHECKLIST.md](SETUP_CHECKLIST.md) - Checklist détaillée
- [my_hfspace/README.md](my_hfspace/README.md) - Doc API

---

## 🎯 Next steps

1. ✅ Préparer vos modèles
2. ✅ Configurer features.json
3. ✅ Déployer sur HF
4. ✅ Tester API
5. ✅ Lancer Django
6. ✅ Customiser l'UI
7. ✅ Ajouter une map

Besoin d'aide? Consulter les guides complets! 📖
