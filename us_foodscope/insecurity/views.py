from django.shortcuts import render
from django.http import JsonResponse
from users.decorators import prediction_access_required
from .forms import FoodInsecurityPredictionForm
from .models import FoodInsecurityPredictionHistory
from .services import FoodInsecurityPredictionService
import json
import pandas as pd
import os

from django.conf import settings
import requests
from io import StringIO


@prediction_access_required('insecurity')
def insecurity_view(request):
    """
    Handle food insecurity prediction form submission.
    Process: 1. Collect form data
             2. Send to prediction service
             3. Save prediction history
             4. Display results
    """
    form = FoodInsecurityPredictionForm()
    prediction_result = None
    risk_level = None
    risk_color = None
    confidence = None
    error_message = None
    prediction_history = []
    
    if request.method == 'POST':
        form = FoodInsecurityPredictionForm(request.POST)
        
        if form.is_valid():
            try:
                # Get raw inputs from cleaned_data
                raw_inputs = {k: v for k, v in form.cleaned_data.items()}
                
                # Call prediction service
                api_response = FoodInsecurityPredictionService.predict(raw_inputs)
                
                if 'error' in api_response:
                    error_message = f"Prediction Error: {api_response.get('details', 'Unknown error')}"
                else:
                    prediction_result = api_response.get('prediction')
                    risk_level = api_response.get('risk_level')
                    risk_color = api_response.get('risk_color')
                    confidence = api_response.get('confidence')
                    
                    # Save to prediction history
                    if request.user.is_authenticated:
                        try:
                            FoodInsecurityPredictionHistory.objects.create(
                                user=request.user,
                                prediction_value=prediction_result,
                                risk_level=risk_level.lower(),
                                input_data=raw_inputs,
                                confidence=confidence or 0.0
                            )
                        except Exception as e:
                            print(f"Error saving prediction history: {e}")
                            
            except Exception as e:
                error_message = f"Application Error: {str(e)}"
    else:
        # GET request: Check for reload history
        load_id = request.GET.get('load_id')
        initial_data = {}
        if load_id and request.user.is_authenticated:
            try:
                hist_item = FoodInsecurityPredictionHistory.objects.get(id=load_id, user=request.user)
                if hist_item.input_data:
                    initial_data = hist_item.input_data
            except FoodInsecurityPredictionHistory.DoesNotExist:
                pass
        
        if initial_data:
            form = FoodInsecurityPredictionForm(initial=initial_data)
    
    # Get prediction history for display
    if request.user.is_authenticated:
        prediction_history = FoodInsecurityPredictionHistory.objects.filter(user=request.user).order_by('-created_at')[:5]
    
    context = {
        'form': form,
        'prediction_result': prediction_result,
        'risk_level': risk_level,
        'risk_color': risk_color,
        'confidence': confidence,
        'error_message': error_message,
        'prediction_history': prediction_history,
    }
    
    return render(request, 'insecurity/insecurity.html', context)


@prediction_access_required('insecurity')
def food_clustering_view(request):
    """
    Render the food insecurity clustering map page.
    """
    return render(request, 'insecurity/clustering.html')


@prediction_access_required('insecurity')
def clustering_data_api(request):
    try:
        csv_url = f"{settings.HF_INSECURITY_API_URL}/county_clusters.csv"

        response = requests.get(csv_url, timeout=10)
        response.raise_for_status()

        df = pd.read_csv(StringIO(response.text))

        counties_data = []
        for _, row in df.iterrows():
            counties_data.append({
                'id': f"{row['State']}|{row['County']}",
                'county': str(row['County']),
                'state': str(row['State']),
                'cluster': int(row['Cluster']),
                'risk_label': str(row['risk_label']),
                'risk_color': str(row['risk_color']),
            })

        total = len(counties_data)
        high = sum(c['cluster'] == 1 for c in counties_data)

        return JsonResponse({
            'counties': counties_data,
            'stats': {
                'total': total,
                'high_vulnerability': high,
                'baseline': total - high,
                'high_percentage': (high / total * 100) if total else 0
            }
        })

    except Exception as e:
        return JsonResponse({'error': str(e), 'counties': []}, status=500)
