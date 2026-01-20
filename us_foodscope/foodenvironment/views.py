from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from users.decorators import prediction_access_required
import json
import logging
from .services import FoodEnvironmentPredictionService
from .forms import FoodEnvironmentPredictionForm
from django.conf import settings

logger = logging.getLogger(__name__)

@prediction_access_required('food_env')
def food_env_view(request):
    """
    Affiche la page du formulaire de prédiction
    """
    return render(request, 'foodenvironment/foodenvironment.html')


@require_http_methods(["POST"])
@csrf_exempt
def food_env_predict(request):
    """
    Reçoit les données du formulaire et appelle le service de prédiction
    """
    try:
        # Parse les données JSON
        logger.debug("Incoming request body (bytes): %s", request.body[:2000])
        print(f"[foodenv] Incoming request body: {request.body[:2000]}")
        data = json.loads(request.body)
        logger.debug("Parsed request JSON: %s", data)
        print(f"[foodenv] Parsed request JSON: {data}")
        
        # Valide les features
        is_valid, error_msg = FoodEnvironmentPredictionService.validate_features(data)
        if not is_valid:
            logger.warning("Validation failed: %s", error_msg)
            print(f"[foodenv] Validation failed: {error_msg}")
            response_data = {'success': False, 'error': error_msg}
            response = JsonResponse(response_data, status=400)
            response['Access-Control-Allow-Origin'] = '*'
            logger.debug("Returning (validation error) response: %s", response_data)
            return response
        
        # Appelle le service de prédiction
        result = FoodEnvironmentPredictionService.predict(data)
        logger.debug("Service result: %s", result)
        print(f"[foodenv] Service result: {result}")

        if result.get('success'):
            response_data = {
                'success': True,
                'prediction': result.get('prediction'),
                'raw': result.get('raw')
            }
            response = JsonResponse(response_data)
            response['Access-Control-Allow-Origin'] = '*'
            logger.debug("Returning success response: %s", response_data)
            print(f"[foodenv] Returning success response: {response_data}")
            return response
        else:
            response_data = {
                'success': False,
                'error': result.get('error'),
                'raw': result.get('raw') if isinstance(result, dict) else None
            }
            response = JsonResponse(response_data, status=500)
            response['Access-Control-Allow-Origin'] = '*'
            logger.debug("Returning error response: %s", response_data)
            print(f"[foodenv] Returning error response: {response_data}")
            return response
    
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON format'
        }, status=400)
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Server error: {str(e)}'
        }, status=500)
    
#def food_env_clustering(request):
   # return render(request, 'foodenvironment/clustering.html')
def food_env_clustering(request):
    context = {
        'clustering_api_url': settings.HF_CLUSTERING_ENDPOINT
    }
    return render(request, 'foodenvironment/clustering.html', context)