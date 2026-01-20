"""
Local Food Analysis Views

Handles regression prediction form submission and clustering visualization.
All ML predictions are handled via Remote Inference (Hugging Face Space).
"""

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from users.decorators import prediction_access_required
from .forms import LocalRegressionForm
from .models import RegressionPredictionHistory
from .services import LocalFoodPredictionService
import logging

logger = logging.getLogger(__name__)

# Cluster descriptions for Local Food Analysis
CLUSTER_DESCRIPTIONS = {
    0: {
        'title': 'Low-Income & High-Need Areas',
        'description': 'These regions exhibit high poverty rates and significant food insecurity. Although their economic potential is limited, they could benefit from programs improving food access and support for local farms. However, they are less of a priority for immediate agricultural market development.'
    },
    1: {
        'title': 'Intermediate Areas',
        'description': 'These regions are characterized by moderate agricultural activity. They offer a moderate growth potential for the local food system, particularly through initiatives adapted to existing farms and local demand.'
    },
    2: {
        'title': 'Wealthy & Agricultural Areas',
        'description': 'These counties combine high median income, low poverty, and strong local agricultural activity (farmers\' markets, direct sales). They represent the highest potential regions for the development of the local food system, capable of supporting market expansion, food innovation, and community engagement.'
    }
}


@prediction_access_required('local')
def local_view(request):
    """Legacy view - redirects to regression form."""
    return render(request, 'local/local.html')


@prediction_access_required('local')
def local_regression_view(request):
    """
    Handle local food regression prediction form submission via HF Space.
    
    Process:
    1. Collect form data
    2. Send to HF Space for prediction
    3. Also get cluster assignment
    4. Display results with map visualization
    """
    form = LocalRegressionForm()
    prediction_result = None
    cluster_result = None
    map_data = None
    error_message = None
    
    if request.method == 'POST':
        form = LocalRegressionForm(request.POST)
        
        if form.is_valid():
            try:
                # Get raw inputs from form
                raw_inputs = {k: v for k, v in form.cleaned_data.items()}
                
                logger.info(f"Form validated successfully with {len(raw_inputs)} fields")
                
                # --- CALL REMOTE SERVICE FOR REGRESSION ---
                api_response = LocalFoodPredictionService.predict(raw_inputs)
                
                if 'error' in api_response:
                    error_message = f"Prediction Error: {api_response.get('details', 'Unknown error')}"
                    
                    # Return JSON if AJAX request
                    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                        return JsonResponse({'success': False, 'message': error_message}, status=400)
                else:
                    prediction_result = {
                        'value': api_response.get('prediction'),
                        'confidence': api_response.get('confidence'),
                        'model': api_response.get('model', 'XGBoost Regressor')
                    }
                    
                    # --- CALL REMOTE SERVICE FOR CLUSTERING ---
                    cluster_response = LocalFoodPredictionService.predict_cluster(raw_inputs)
                    
                    if 'error' not in cluster_response:
                        cluster_result = {
                            'cluster': cluster_response.get('cluster'),
                            'confidence': cluster_response.get('confidence', 0.75)
                        }
                    
                    # --- SAVE HISTORY ---
                    if request.user.is_authenticated:
                        try:
                            RegressionPredictionHistory.objects.create(
                                user=request.user,
                                input_data=raw_inputs,
                                prediction_value=prediction_result['value'],
                                confidence_score=prediction_result['confidence'],
                                cluster_assigned=cluster_result['cluster'] if cluster_result else None,
                                cluster_probability=cluster_result['confidence'] if cluster_result else None
                            )
                        except Exception as e:
                            logger.error(f"Error saving prediction history: {e}")
                    
                    # Return JSON if AJAX request
                    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                        return JsonResponse({
                            'success': True,
                            'prediction': prediction_result['value'],
                            'confidence': prediction_result['confidence'],
                            'cluster': cluster_result['cluster'] if cluster_result else None,
                            'cluster_confidence': cluster_result['confidence'] if cluster_result else None
                        })
                    
            except Exception as e:
                error_message = f"Application Error: {str(e)}"
                logger.error(f"Local regression view error: {e}")
                
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({'success': False, 'message': error_message}, status=500)
        else:
            # Form validation failed
            error_message = "Please fill in all required fields correctly."
            logger.warning(f"Form validation failed: {form.errors}")
            for field, errors in form.errors.items():
                logger.warning(f"  {field}: {errors}")
    
    # GET Request: Load from history if requested
    if request.method == 'GET':
        load_id = request.GET.get('load_id')
        initial_data = {}
        if load_id and request.user.is_authenticated:
            try:
                hist_item = RegressionPredictionHistory.objects.get(id=load_id, user=request.user)
                if hist_item.input_data:
                    initial_data = hist_item.input_data
            except RegressionPredictionHistory.DoesNotExist:
                pass
        
        if initial_data:
            form = LocalRegressionForm(initial=initial_data)
    
    # Get prediction history
    prediction_history = []
    if request.user.is_authenticated:
        prediction_history = RegressionPredictionHistory.objects.filter(
            user=request.user
        ).order_by('-created_at')[:5]
    
    # Get field groups for template
    field_groups = form.get_field_groups() if hasattr(form, 'get_field_groups') else {}
    
    # Add cluster description if result exists
    cluster_info = None
    if cluster_result and 'cluster' in cluster_result:
        cluster_num = cluster_result.get('cluster')
        if cluster_num in CLUSTER_DESCRIPTIONS:
            cluster_info = CLUSTER_DESCRIPTIONS[cluster_num]
    
    context = {
        'form': form,
        'field_groups': field_groups,
        'prediction_result': prediction_result,
        'cluster_result': cluster_result,
        'cluster_info': cluster_info,
        'map_data': map_data,
        'error_message': error_message,
        'prediction_history': prediction_history,
    }
    
    return render(request, 'local/regression.html', context)


@require_http_methods(["GET"])
@prediction_access_required('local')
def clustering_map_view(request):
    """
    API endpoint to get clustering data for map visualization.
    Returns JSON with county coordinates and cluster assignments.
    """
    map_data = LocalFoodPredictionService.get_clustering_map_data()
    
    if 'error' in map_data:
        return JsonResponse(
            {'error': map_data.get('details', 'Failed to load map data')},
            status=500
        )
    
    return JsonResponse(map_data)


@prediction_access_required('local')
def local_clustering_view(request):
    """
    Handle local food clustering analysis form submission via HF Space.
    
    Process:
    1. Collect form data
    2. Send to HF Space for cluster assignment
    3. Display cluster results with confidence score
    """
    form = LocalRegressionForm()
    cluster_result = None
    error_message = None
    
    if request.method == 'POST':
        form = LocalRegressionForm(request.POST)
        
        if form.is_valid():
            try:
                # Get raw inputs from form
                raw_inputs = {k: v for k, v in form.cleaned_data.items()}
                
                # Get cluster prediction from service
                cluster_result = LocalFoodPredictionService.predict_cluster(raw_inputs)
                
                if 'error' in cluster_result:
                    error_message = str(cluster_result.get('error'))
                    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                        return JsonResponse({'success': False, 'message': error_message}, status=400)
                else:
                    # Save to history
                    if request.user.is_authenticated:
                        try:
                            RegressionPredictionHistory.objects.create(
                                user=request.user,
                                input_data=raw_inputs,
                                prediction_value=cluster_result.get('cluster', 0),
                                confidence_score=cluster_result.get('confidence', 0.0),
                                cluster_assigned=cluster_result.get('cluster'),
                                cluster_probability=cluster_result.get('confidence', 0.0)
                            )
                        except Exception as e:
                            logger.error(f"Error saving clustering history: {e}")
                    
                    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                        return JsonResponse({
                            'success': True,
                            'cluster': cluster_result.get('cluster'),
                            'confidence': cluster_result.get('confidence', 0.0)
                        })
                    
            except Exception as e:
                error_message = str(e)
                logger.error(f"Clustering error: {error_message}")
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({'success': False, 'message': error_message}, status=500)
    
    # Get field groups for template
    field_groups = form.get_field_groups() if hasattr(form, 'get_field_groups') else {}
    
    # Add cluster description if result exists
    cluster_info = None
    if cluster_result and 'cluster' in cluster_result:
        cluster_num = cluster_result.get('cluster')
        if cluster_num in CLUSTER_DESCRIPTIONS:
            cluster_info = CLUSTER_DESCRIPTIONS[cluster_num]
    
    # Get clustering history
    clustering_history = []
    if request.user.is_authenticated:
        clustering_history = RegressionPredictionHistory.objects.filter(
            user=request.user
        ).exclude(cluster_assigned__isnull=True).order_by('-created_at')[:5]
    
    context = {
        'form': form,
        'field_groups': field_groups,
        'cluster_result': cluster_result,
        'cluster_info': cluster_info,
        'error_message': error_message,
        'clustering_history': clustering_history,
    }
    return render(request, 'local/clustering.html', context)

