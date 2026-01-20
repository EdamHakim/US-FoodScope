"""
Finance Prediction View

Handles form submission and ML predictions via Remote Inference.
"""
from django.shortcuts import render
from django.http import JsonResponse
from users.decorators import prediction_access_required
from .forms import FinancePredictionForm
from .models import PredictionHistory
from .services import FinancePredictionService
import json


@prediction_access_required('finance')
def finance_view(request):
    """
    Handle finance prediction form submission via Remote Inference (Hugging Face).
    
    Process:
    1. Collect form data
    2. Send raw data to HF Space
    3. Display results
    """
    form = FinancePredictionForm()
    prediction_result = None
    prediction_probability = None
    selected_model = None
    error_message = None
    
    if request.method == 'POST':
        print("=" * 50)
        print("POST REQUEST RECEIVED - PREDICTIONS")
        print("POST data:", request.POST)
        print("=" * 50)
        
        form = FinancePredictionForm(request.POST)
        
        print("Form is valid:", form.is_valid())
        if not form.is_valid():
            print("Form errors:", form.errors)
        
        if form.is_valid():
            try:
                # Get raw inputs directly from cleaned_data
                raw_inputs = {k: v for k, v in form.cleaned_data.items()}
                print("Cleaned data:", raw_inputs)
                
                # Determine model type
                model_type = raw_inputs.get('model_type', 'tax_rate')
                selected_model = 'Tax Rate'
                
                print(f"Model type: {model_type}")
                print(f"Selected model: {selected_model}")
                
                # CALL REMOTE SERVICE
                print("Calling remote service...")
                api_response = FinancePredictionService.predict(model_type, raw_inputs)
                print("API Response:", api_response)
                
                if 'error' in api_response:
                    error_message = f"Remote Inference Error: {api_response.get('details', 'Unknown error')}"
                    print("Error from API:", error_message)
                else:
                    prediction_result = api_response.get('prediction')
                    prediction_probability = api_response.get('probability')
                    
                    print(f"Prediction result: {prediction_result}")
                    print(f"Probability: {prediction_probability}")
                    
                    # --- SAVE HISTORY ---
                    if request.user.is_authenticated:
                        try:
                            history_entry = PredictionHistory.objects.create(
                                user=request.user,
                                model_type=model_type,
                                prediction_value=prediction_result,
                                input_data=raw_inputs,
                                confidence_interval=prediction_probability or ""
                            )
                            print(f"History saved with ID: {history_entry.id}")
                        except Exception as e:
                            print(f"Error saving history: {e}")
                                
            except Exception as e:
                error_message = f"Application Error: {str(e)}"
                print("Exception occurred:", error_message)
                import traceback
                traceback.print_exc()
        else:
            error_message = "Please correct the errors in the form."
    else:
        # GET Request: Check for reload history
        load_id = request.GET.get('load_id')
        initial_data = {}
        if load_id and request.user.is_authenticated:
            try:
                hist_item = PredictionHistory.objects.get(id=load_id, user=request.user)
                if hist_item.input_data:
                    initial_data = hist_item.input_data
                    print(f"Loading history item {load_id}:", initial_data)
            except PredictionHistory.DoesNotExist:
                print(f"History item {load_id} not found")
                pass
        
        form = FinancePredictionForm(initial=initial_data)

    # --- GET HISTORY FOR CONTEXT (only tax_rate) ---
    prediction_history = []
    if request.user.is_authenticated:
        prediction_history = PredictionHistory.objects.filter(
            user=request.user,
            model_type='tax_rate'
        ).order_by('-created_at')[:5]
        print(f"Found {len(prediction_history)} prediction history items")

    context = {
        'form': form,
        'prediction_result': prediction_result,
        'prediction_probability': prediction_probability,
        'selected_model': selected_model,
        'error_message': error_message,
        'prediction_history': prediction_history,
    }
    
    return render(request, 'finance/finance.html', context)


@prediction_access_required('finance')
def clustering_view(request):
    """
    Handle clustering form submission and display map visualization.
    Classifies states into clusters based on socioeconomic indicators.
    """
    form = FinancePredictionForm()
    cluster_result = None
    prediction_probability = None
    error_message = None
    cluster_data = None
    priority_states = None
    
    if request.method == 'POST':
        print("=" * 50)
        print("POST REQUEST RECEIVED - CLUSTERING")
        print("POST data:", request.POST)
        print("=" * 50)
        
        form = FinancePredictionForm(request.POST)
        
        print("Form is valid:", form.is_valid())
        if not form.is_valid():
            print("Form errors:", form.errors)
        
        if form.is_valid():
            try:
                # Get raw inputs directly from cleaned_data
                raw_inputs = {k: v for k, v in form.cleaned_data.items()}
                print("Cleaned data:", raw_inputs)
                
                # Force clustering model type
                model_type = 'clustering'
                raw_inputs['model_type'] = model_type
                
                print(f"Model type: {model_type}")
                
                # CALL REMOTE SERVICE
                print("Calling remote clustering service...")
                api_response = FinancePredictionService.predict(model_type, raw_inputs)
                print("API Response:", api_response)
                
                if 'error' in api_response:
                    error_message = f"Remote Inference Error: {api_response.get('details', 'Unknown error')}"
                    print("Error from API:", error_message)
                else:
                    cluster_result = api_response.get('prediction')
                    prediction_probability = api_response.get('probability')
                    
                    # Get cluster data for map visualization
                    cluster_data = api_response.get('cluster_data', [])
                    priority_states = api_response.get('priority_states', [])
                    
                    print(f"Cluster result: {cluster_result}")
                    print(f"Probability: {prediction_probability}")
                    print(f"Cluster data count: {len(cluster_data) if cluster_data else 0}")
                    print(f"Priority states count: {len(priority_states) if priority_states else 0}")
                    
                    # --- SAVE HISTORY ---
                    if request.user.is_authenticated:
                        try:
                            history_entry = PredictionHistory.objects.create(
                                user=request.user,
                                model_type=model_type,
                                prediction_value=str(cluster_result),
                                input_data=raw_inputs,
                                confidence_interval=prediction_probability or ""
                            )
                            print(f"Clustering history saved with ID: {history_entry.id}")
                        except Exception as e:
                            print(f"Error saving history: {e}")
                                
            except Exception as e:
                error_message = f"Application Error: {str(e)}"
                print("Exception occurred:", error_message)
                import traceback
                traceback.print_exc()
        else:
            error_message = "Please correct the errors in the form."
    else:
        # GET Request: Check for reload history
        load_id = request.GET.get('load_id')
        initial_data = {}
        if load_id and request.user.is_authenticated:
            try:
                hist_item = PredictionHistory.objects.get(id=load_id, user=request.user)
                if hist_item.input_data:
                    initial_data = hist_item.input_data
                    print(f"Loading clustering history item {load_id}:", initial_data)
            except PredictionHistory.DoesNotExist:
                print(f"Clustering history item {load_id} not found")
                pass
        
        form = FinancePredictionForm(initial=initial_data)

    # Convert cluster_data to JSON for JavaScript
    cluster_data_json = json.dumps(cluster_data) if cluster_data else 'null'
    
    print(f"Cluster data JSON length: {len(cluster_data_json) if cluster_data_json else 0}")

    context = {
        'form': form,
        'cluster_result': cluster_result,
        'prediction_probability': prediction_probability,
        'error_message': error_message,
        'cluster_data': cluster_data_json,
        'priority_states': priority_states,
    }
    
    return render(request, 'finance/clustering.html', context)


@prediction_access_required('finance')
def clustering_data_api(request):
    """
    API endpoint to serve clustering data as JSON for map visualization.
    Future enhancement: load actual clustering data from database
    """
    # This would typically fetch from your database
    # For now, return empty data
    data = []
    return JsonResponse({'states': data})