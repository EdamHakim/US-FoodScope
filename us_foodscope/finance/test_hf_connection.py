from django.test import TestCase

# Create your tests here.
"""
Quick test script to verify your Hugging Face Space connection
Run this BEFORE integrating into Django to make sure everything works
"""

from gradio_client import Client

# Your Hugging Face Space URL
SPACE_URL = "https://mariem08-fml-models.hf.space"

def test_connection():
    """Test basic connection to your Space"""
    print("=" * 60)
    print(" Testing Hugging Face Space Connection")
    print("=" * 60)
    print(f" Space URL: {SPACE_URL}")
    print()
    
    try:
        print(" Connecting to Gradio Space...")
        client = Client(SPACE_URL)
        print(" Successfully connected!")
        print()
        
        # Get API info
        print(" Fetching API endpoints...")
        print(f"   Available endpoints: {client.endpoints}")
        print()
        
        return True
        
    except Exception as e:
        print(f" Connection failed: {e}")
        print()
        print(" Troubleshooting tips:")
        print("   1. Check if your Space is running: visit the URL in your browser")
        print("   2. If it says 'Building' or 'Sleeping', wait a few minutes")
        print("   3. Make sure your Space is public (not private)")
        print("   4. Check your internet connection")
        return False


def test_tax_prediction():
    """Test tax rate prediction"""
    print("=" * 60)
    print(" Testing Tax Rate Prediction")
    print("=" * 60)
    
    try:
        client = Client(SPACE_URL)
        
        # Sample input - UPDATE these values to match your features
        print(" Sending test data...")
        result = client.predict(
            10,  # Adult_Obesity_Rate13
            10,  # Adult_Diabetes_Rate13
            10,  # Adult_Obesity_Rate_08
            10,  # Adult_Diabetes_Rate_08
            0,   # SODATAX_STORES14
            0,   # CHIPSTAX_VENDM14
            0,   # PCT_LOCLFARM12
            0,   # VLFOODSEC_10_12
            api_name="/predict_tax"
        )
        
        print(" Result received:")
        print(result)
        print()
        print(" Tax prediction test PASSED!")
        return True
        
    except Exception as e:
        print(f" Tax prediction test FAILED: {e}")
        print()
        print(" Tips:")
        print("   1. Check if api_name '/predict_tax' exists in your app.py")
        print("   2. Verify the number of inputs matches your Gradio interface")
        print("   3. Make sure you updated app.py with api_name parameters")
        return False


def test_clustering():
    """Test clustering prediction"""
    print("=" * 60)
    print(" Testing Clustering Prediction")
    print("=" * 60)
    
    try:
        client = Client(SPACE_URL)
        
        # Sample input - UPDATE these to match your clustering features
        print(" Sending test data...")
        result = client.predict(
            50000,  # Median_Income
            0,      # FoodInsec_13_15
            0,      # Adult_Obesity_Rate13
            api_name="/predict_cluster"
        )
        
        print(" Result received:")
        print(result[0] if isinstance(result, tuple) else result)
        print()
        print(" Clustering test PASSED!")
        return True
        
    except Exception as e:
        print(f" Clustering test FAILED: {e}")
        print()
        print(" Tips:")
        print("   1. Check if api_name '/predict_cluster' exists in your app.py")
        print("   2. Verify the number of inputs matches your clustering interface")
        return False


if __name__ == "__main__":
    print()
    print(" Starting Hugging Face Space Tests")
    print()
    
    # Test 1: Connection
    if not test_connection():
        print("\n Cannot proceed with tests - connection failed")
        print("Please fix the connection issue first!")
        exit(1)
    
    print()
    input("Press Enter to test tax prediction...")
    print()
    
    # Test 2: Tax Prediction
    test_tax_prediction()
    
    print()
    input("Press Enter to test clustering...")
    print()
    
    # Test 3: Clustering
    test_clustering()
    
    print()
    print("=" * 60)
    print(" All tests completed!")
    print("=" * 60)
    print()
    print(" Next steps:")
    print("   1. If all tests passed: integrate into Django ")
    print("   2. If any test failed: check the error messages above ")
    print()
    print(" To integrate into Django:")
    print("   1. Copy services_api.py to finance/")
    print("   2. Copy forms_simple.py to finance/forms.py")
    print("   3. Copy views_api.py to finance/views.py")
    print("   4. Update settings.py with HF_FINANCE_SPACE_URL")
    print("   5. Run: python manage.py runserver")
    print()