from huggingface_hub import hf_hub_download
import joblib
import os

REPO_ID = "tasnime22/us-foodscope-access-models"

LOCAL_DIR = os.path.join(os.path.dirname(__file__), "ml_models")
os.makedirs(LOCAL_DIR, exist_ok=True)


def load_model(filename):
    path = hf_hub_download(
        repo_id=REPO_ID,
        filename=filename,
        local_dir=LOCAL_DIR,
        local_dir_use_symlinks=False
    )
    return joblib.load(path)


# ✅ Prediction
reg_model = load_model("best_reg_model.joblib")
clf_model = load_model("best_clf_model.joblib")

# ✅ Clustering (unsupervised)
kmeans_model = load_model("kmeans_unsup_model.joblib")
pca_model = load_model("unsup_pca.joblib")
scaler_model = load_model("unsup_scaler.joblib")
