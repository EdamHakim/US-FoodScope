"""
ML Artifacts Loader - Lightweight JSON Version

Loads pre-extracted categorical choices from JSON to populate forms
without requiring scikit-learn or joblib to be installed.
"""

import json
import os
from pathlib import Path
from django.conf import settings

BASE_DIR = Path(__file__).resolve().parent
CHOICES_FILE = BASE_DIR / 'encoder_choices.json'

def load_encoder_choices():
    """
    Load categorical choices from JSON file.
    Returns: dict mapping feature_name -> list of choices
    """
    if CHOICES_FILE.exists():
        try:
            with open(CHOICES_FILE, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading encoder choices: {e}")
    return {}

# Load choices into a global variable
ENCODER_CHOICES = load_encoder_choices()

