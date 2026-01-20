"""
Upload Script for Hugging Face Spaces

This script uploads all necessary files to your Hugging Face Space.

Prerequisites:
1. Install huggingface_hub: pip install huggingface_hub
2. Have your trained models in the current directory:
   - xgboost_tuned_model.joblib
   - kmeans_model.pkl
   - scaler_regression.pkl
   - scaler.pkl
   - scaled_columns.pkl
   - clustering_features.json
3. Create a .env file with your HF token or use `huggingface-cli login`

Usage:
    python upload_models.py
"""

import os
import sys
from pathlib import Path
from huggingface_hub import login, HfApi

def main():
    """Upload files to Hugging Face Space."""
    
    # Configuration
    HF_SPACE_NAME = "rouazekri-roua-localfood"  # Your space name
    HF_USERNAME = "rouazekri"  # Your HF username
    
    # Files to upload
    required_files = [
        "app.py",
        "Dockerfile",
        "requirements.txt",
        "xgboost_tuned_model.joblib",
        "kmeans_model.pkl",
        "scaler_regression.pkl",
        "scaler.pkl",
        "scaled_columns.pkl",
        "clustering_features.json",
    ]
    
    optional_files = [
        "clustering_map_data.json",
        "generate_config.py",
        "README.md",
    ]
    
    print("🚀 Uploading to Hugging Face Space...")
    print(f"Space: {HF_USERNAME}/{HF_SPACE_NAME}")
    print()
    
    # Check required files
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"   - {file}")
        print("\n⚠️  Please ensure all required files are in the current directory.")
        print("   Required files:")
        for file in required_files:
            print(f"   - {file}")
        sys.exit(1)
    
    # Check optional files and warn
    for file in optional_files:
        if not Path(file).exists():
            print(f"⚠️  Optional file missing: {file}")
    
    print()
    print("✅ All required files found.")
    print()
    
    # Login to HF
    try:
        print("🔐 Authenticating with Hugging Face...")
        login()
        print("✅ Authentication successful")
    except Exception as e:
        print(f"❌ Authentication failed: {e}")
        print("   Run 'huggingface-cli login' first")
        sys.exit(1)
    
    print()
    
    # Create API client
    api = HfApi()
    
    # Upload each file
    current_dir = Path(".")
    
    for file in required_files + optional_files:
        file_path = current_dir / file
        if file_path.exists():
            try:
                print(f"📤 Uploading {file}...", end=" ")
                api.upload_file(
                    path_or_fileobj=str(file_path),
                    path_in_repo=file,
                    repo_id=f"{HF_USERNAME}/{HF_SPACE_NAME}",
                    repo_type="space"
                )
                print("✅")
            except Exception as e:
                print(f"❌ {e}")
                sys.exit(1)
    
    print()
    print("✅ All files uploaded successfully!")
    print(f"   Space URL: https://huggingface.co/spaces/{HF_USERNAME}/{HF_SPACE_NAME}")
    print()
    print("📋 Next steps:")
    print("   1. Go to your HF Space settings")
    print("   2. Configure Docker runtime if not already done")
    print("   3. Monitor the build logs")
    print("   4. Test the API once deployed")


if __name__ == "__main__":
    main()
