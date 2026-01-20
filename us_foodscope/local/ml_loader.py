"""
ML Artifacts Loader for Local Food Regression

Loads feature configuration and clustering data from JSON files.
"""

import json
import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
CLUSTERING_FEATURES_FILE = BASE_DIR / 'my_hfspace' / 'clustering_features.json'


def load_clustering_features():
    """
    Load clustering feature definitions from JSON file.
    
    Returns:
        dict: Feature definitions with type, min, max, categories, etc.
    """
    if CLUSTERING_FEATURES_FILE.exists():
        try:
            with open(CLUSTERING_FEATURES_FILE, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading clustering features: {e}")
    return {}


# Load features into a global variable
CLUSTERING_FEATURES = load_clustering_features()
