"""
Feature Configuration Builder for Clustering

This script creates a comprehensive feature configuration JSON file
that describes all clustering features used in the model.

Run this once to generate clustering_features.json from your training data.
"""

import json
from pathlib import Path


def create_feature_config():
    """
    Create feature configuration for local food clustering.
    
    Customize this based on your actual features and their properties.
    """
    
    # Example configuration - MODIFY ACCORDING TO YOUR ACTUAL FEATURES
    features_config = {
        "feature_1": {
            "display_name": "Feature 1 Name",
            "description": "Description of feature 1",
            "type": "numeric",
            "min": 0,
            "max": 100,
            "unit": "units"
        },
        "feature_2": {
            "display_name": "Feature 2 Name",
            "description": "Description of feature 2",
            "type": "numeric",
            "min": -50,
            "max": 50,
            "unit": "units"
        },
        "category_feature": {
            "display_name": "Category Feature",
            "description": "A categorical feature",
            "type": "categorical",
            "categories": ["category_a", "category_b", "category_c"]
        }
        # Add more features as needed
    }
    
    return features_config


def create_clustering_map_template():
    """
    Create template for clustering map data.
    
    This should contain county/region information with cluster assignments.
    """
    map_data = {
        "clusters": {
            "0": {
                "name": "Cluster 0",
                "description": "Description of cluster 0",
                "centroid": {
                    "x": 0.5,
                    "y": 0.5
                },
                "color": "#FF6B6B",
                "counties": []  # Add county IDs or names
            },
            "1": {
                "name": "Cluster 1",
                "description": "Description of cluster 1",
                "centroid": {
                    "x": -0.5,
                    "y": 0.5
                },
                "color": "#4ECDC4",
                "counties": []
            }
            # Add more clusters as needed
        },
        "metadata": {
            "total_counties": 0,
            "total_clusters": 2,
            "feature_scaling": "StandardScaler"
        }
    }
    
    return map_data


if __name__ == "__main__":
    # Generate feature config
    features = create_feature_config()
    
    # Save to JSON
    config_path = Path(__file__).parent / "clustering_features.json"
    with open(config_path, 'w') as f:
        json.dump(features, f, indent=2)
    
    print(f"✅ Feature configuration saved to {config_path}")
    
    # Generate map data template
    map_data = create_clustering_map_template()
    
    map_path = Path(__file__).parent / "clustering_map_data.json"
    with open(map_path, 'w') as f:
        json.dump(map_data, f, indent=2)
    
    print(f"✅ Clustering map template saved to {map_path}")
    print("\n📝 IMPORTANT: Update these JSON files with your actual features and clustering data!")
