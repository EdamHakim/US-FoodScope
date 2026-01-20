
import joblib
import os
import sys

def inspect_model(filename):
    print(f"--- Inspecting {filename} ---")
    if not os.path.exists(filename):
        print("File not found.")
        return

    try:
        model = joblib.load(filename)
        print(f"Type: {type(model)}")
        
        if hasattr(model, 'feature_names_in_'):
            print("Feature Names In:", list(model.feature_names_in_))
        else:
            print("No 'feature_names_in_' attribute.")
            
        if hasattr(model, 'n_features_in_'):
            print("N Features In:", model.n_features_in_)
            
        if hasattr(model, 'mean_'):
            print("Scaler Mean (first 5):", model.mean_[:5])
        
        if hasattr(model, 'cluster_centers_'):
            print("Cluster Centers Shape:", model.cluster_centers_.shape)

    except Exception as e:
        print(f"Error loading: {e}")

if __name__ == "__main__":
    inspect_model('clustering_scaler.joblib')
    # Try probable names if list_dir was truncated
    inspect_model('kmeans_health_model.joblib')
    inspect_model('kmeans_model.joblib') 
