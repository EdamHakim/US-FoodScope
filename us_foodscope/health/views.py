"""
Health Prediction View

Handles form submission, feature encoding/scaling, and ML predictions.
All ML artifacts are pre-loaded and reused - never retrained or refit.
"""

from django.shortcuts import render
from django.http import JsonResponse
from users.decorators import prediction_access_required
from users.decorators import prediction_access_required
from .forms import HealthPredictionForm, ClusteringForm
from .models import PredictionHistory
from .services import HealthPredictionService
@prediction_access_required('health')
def health_view(request):
    """
    Handle health prediction form submission via Remote Inference (Hugging Face).
    
    Process:
    1. Collect form data
    2. Send raw data to Helper Service (HF Space)
    3. Display results
    """
    form = HealthPredictionForm()
    prediction_result = None
    prediction_probability = None
    selected_model = None
    error_message = None
    
    if request.method == 'POST':
        form = HealthPredictionForm(request.POST)
        
        if form.is_valid():
            try:
                # Get raw inputs directly from cleaned_data
                # The Service/API handles encoding and scaling now
                raw_inputs = {k: v for k, v in form.cleaned_data.items()}
                
                # Determine model type
                model_type = raw_inputs.get('model_type', 'obesity')
                selected_model = 'Obesity' if model_type == 'obesity' else 'Diabetes'
                
                # CALL REMOTE SERVICE
                api_response = HealthPredictionService.predict(model_type, raw_inputs)
                
                if 'error' in api_response:
                    error_message = f"Remote Inference Error: {api_response.get('details', 'Unknown error')}"
                else:
                    prediction_result = api_response.get('prediction')
                    prediction_probability = api_response.get('probability')
                    
                    # --- SAVE HISTORY ---
                    if request.user.is_authenticated:
                        try:
                            PredictionHistory.objects.create(
                                user=request.user,
                                model_type=model_type,
                                prediction_value=prediction_result,
                                risk_level_input=str(raw_inputs.get('Risk_Level', 'N/A')),
                                input_data=raw_inputs,
                                confidence_interval=prediction_probability or ""
                            )
                        except Exception as e:
                            print(f"Error saving history: {e}")
                                
            except Exception as e:
                error_message = f"Application Error: {str(e)}"
    else:
        # GET Request: Check for reload history
        load_id = request.GET.get('load_id')
        initial_data = {}
        if load_id and request.user.is_authenticated:
            try:
                hist_item = PredictionHistory.objects.get(id=load_id, user=request.user)
                if hist_item.input_data:
                    initial_data = hist_item.input_data
            except PredictionHistory.DoesNotExist:
                pass
        
        form = HealthPredictionForm(initial=initial_data)

    # --- GET HISTORY FOR CONTEXT ---
    prediction_history = []
    if request.user.is_authenticated:
        prediction_history = PredictionHistory.objects.filter(user=request.user).order_by('-created_at')[:5]

    context = {
        'form': form,
        'prediction_result': prediction_result,
        'prediction_probability': prediction_probability,
        'selected_model': selected_model,
        'error_message': error_message,
        'prediction_history': prediction_history,
    }
    
    return render(request, 'health/health.html', context)


@prediction_access_required('health')
def clustering_view(request):
    """
    Render the clustering map page and handle K-Means prediction.
    """
    form = ClusteringForm()
    cluster_result = None
    cluster_desc = None
    error_message = None

    # Cluster descriptions
    CLUSTER_DESCRIPTIONS = {
        0: "Healthiest Profile",
        1: "Highest Risk (Priority Intervention)",
        2: "Moderate Profile",
        3: "Mixed Profile"
    }

    if request.method == 'POST':
        form = ClusteringForm(request.POST)
        if form.is_valid():
            try:
                # Extract inputs
                raw_inputs = {k: v for k, v in form.cleaned_data.items()}
                
                # Call Service
                print(f"DEBUG: Clustering Input Features: {raw_inputs}")
                api_response = HealthPredictionService.predict_cluster(raw_inputs)
                print(f"DEBUG: Clustering API Response: {api_response}")
                
                if 'error' in api_response:
                    error_message = f"Clustering Error: {api_response.get('details')}"
                else:
                    cluster_result = api_response.get('cluster')
                    cluster_desc = CLUSTER_DESCRIPTIONS.get(cluster_result, "Unknown Cluster")
            except Exception as e:
                print(f"DEBUG: Clustering Exception: {e}")
                error_message = f"Application Error: {str(e)}"
    
    context = {
        'form': form,
        'cluster_result': cluster_result,
        'cluster_desc': cluster_desc,
        'error_message': error_message
    }
    return render(request, 'health/clustering.html', context)


@prediction_access_required('health')
def clustering_data_api(request):
    """
    API endpoint to serve clustering data as JSON.
    """
    from .services import load_clustering_data
    data = load_clustering_data()
    return JsonResponse({'counties': data})
