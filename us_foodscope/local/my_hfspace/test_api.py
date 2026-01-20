"""
Test Script for Local Food API

This script tests all endpoints of the deployed HF Space API.
"""

import requests
import json
from typing import Dict, Any


class LocalFoodAPITester:
    """Test local food inference API."""
    
    def __init__(self, api_url: str = "https://rouazekri-roua-localfood.hf.space"):
        self.api_url = api_url
        self.session = requests.Session()
        self.results = []
    
    def test_health_check(self) -> bool:
        """Test the health check endpoint."""
        print("\n🔍 Testing Health Check...")
        try:
            response = self.session.get(f"{self.api_url}/health", timeout=5)
            response.raise_for_status()
            data = response.json()
            
            print(f"✅ Status: {response.status_code}")
            print(f"   Response: {json.dumps(data, indent=2)}")
            
            if data.get('status') == 'ok':
                print(f"   ✓ API is healthy")
                return True
            else:
                print(f"   ✗ Unexpected response")
                return False
                
        except Exception as e:
            print(f"❌ Health check failed: {e}")
            return False
    
    def test_prediction(self, features: Dict[str, Any]) -> bool:
        """Test the prediction endpoint."""
        print("\n🎯 Testing Prediction Endpoint...")
        try:
            payload = {"features": features}
            
            print(f"   Sending request with features: {list(features.keys())}")
            
            response = self.session.post(
                f"{self.api_url}/predict",
                json=payload,
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            
            print(f"✅ Status: {response.status_code}")
            print(f"   Prediction: {data.get('prediction')}")
            print(f"   Confidence: {data.get('confidence')}")
            print(f"   Model: {data.get('model_used')}")
            
            return True
            
        except Exception as e:
            print(f"❌ Prediction failed: {e}")
            return False
    
    def test_clustering(self, features: Dict[str, Any]) -> bool:
        """Test the clustering endpoint."""
        print("\n🗂️  Testing Clustering Endpoint...")
        try:
            payload = {"features": features}
            
            print(f"   Sending request with features: {list(features.keys())}")
            
            response = self.session.post(
                f"{self.api_url}/cluster",
                json=payload,
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            
            print(f"✅ Status: {response.status_code}")
            print(f"   Cluster: {data.get('cluster')}")
            print(f"   Probability: {data.get('probability')}")
            print(f"   Coordinates: {data.get('coordinates')}")
            
            return True
            
        except Exception as e:
            print(f"❌ Clustering failed: {e}")
            return False
    
    def test_clustering_map(self) -> bool:
        """Test the clustering map endpoint."""
        print("\n🗺️  Testing Clustering Map Endpoint...")
        try:
            response = self.session.get(
                f"{self.api_url}/clustering-map",
                timeout=5
            )
            response.raise_for_status()
            data = response.json()
            
            print(f"✅ Status: {response.status_code}")
            
            if isinstance(data, dict):
                print(f"   Data keys: {list(data.keys())}")
                if 'clusters' in data:
                    print(f"   Number of clusters: {len(data.get('clusters', {}))}")
            else:
                print(f"   Response type: {type(data)}")
            
            return True
            
        except Exception as e:
            print(f"❌ Clustering map failed: {e}")
            return False
    
    def test_root_endpoint(self) -> bool:
        """Test the root endpoint."""
        print("\n📋 Testing Root Endpoint...")
        try:
            response = self.session.get(f"{self.api_url}/", timeout=5)
            response.raise_for_status()
            data = response.json()
            
            print(f"✅ Status: {response.status_code}")
            print(f"   Message: {data.get('message')}")
            print(f"   Version: {data.get('version')}")
            
            if 'endpoints' in data:
                print(f"   Available endpoints:")
                for endpoint, description in data.get('endpoints', {}).items():
                    print(f"      • {endpoint}: {description}")
            
            return True
            
        except Exception as e:
            print(f"❌ Root endpoint failed: {e}")
            return False
    
    def run_full_test(self, test_features: Dict[str, Any] = None):
        """Run all tests."""
        print("=" * 60)
        print("🚀 Local Food API Test Suite")
        print("=" * 60)
        print(f"API URL: {self.api_url}\n")
        
        # Test basic endpoints
        results = {
            'health': self.test_health_check(),
            'root': self.test_root_endpoint(),
        }
        
        # Only test prediction/clustering if health is good
        if results.get('health'):
            # Use default test features if not provided
            if test_features is None:
                test_features = {
                    "feature_1": 5.2,
                    "feature_2": 10,
                    "feature_3": 20.5,
                    # Add more features as needed
                }
            
            results['prediction'] = self.test_prediction(test_features)
            results['clustering'] = self.test_clustering(test_features)
            results['clustering_map'] = self.test_clustering_map()
        
        # Print summary
        print("\n" + "=" * 60)
        print("📊 Test Summary")
        print("=" * 60)
        
        passed = sum(1 for v in results.values() if v)
        total = len(results)
        
        for test_name, result in results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{status} - {test_name.capitalize()}")
        
        print(f"\nTotal: {passed}/{total} tests passed")
        print("=" * 60)
        
        return passed == total


def main():
    """Main test entry point."""
    import sys
    
    # Allow custom API URL via command line
    api_url = sys.argv[1] if len(sys.argv) > 1 else "https://rouazekri-roua-localfood.hf.space"
    
    # Create tester
    tester = LocalFoodAPITester(api_url)
    
    # Run tests with example features
    # MODIFY THESE BASED ON YOUR ACTUAL FEATURES
    example_features = {
        "population_density": 500.5,
        "median_income": 75000,
        "poverty_rate": 15.5,
        # Add more features as needed based on your model
    }
    
    success = tester.run_full_test(example_features)
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
