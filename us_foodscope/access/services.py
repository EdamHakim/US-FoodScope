import numpy as np
from .ml_loader import reg_model, clf_model, kmeans_model, pca_model, scaler_model


def predict_access(features):
    """
    Regression prediction:
    Predict % limited access population
    """
    X = np.array([features], dtype=float)
    return float(reg_model.predict(X)[0])


def classify_access(features):
    """
    Classification prediction:
    Predict if tract/county is Low-Income Low-Access (1) or not (0)
    """
    X = np.array([features], dtype=float)
    return int(clf_model.predict(X)[0])


def cluster_access(features):
    """
    Clustering prediction:
    Apply scaler -> PCA -> KMeans
    """
    X = np.array([features], dtype=float)

    # ✅ Scale
    X_scaled = scaler_model.transform(X)

    # ✅ PCA
    X_pca = pca_model.transform(X_scaled)

    # ✅ Cluster
    return int(kmeans_model.predict(X_pca)[0])
