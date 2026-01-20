"""
Django Form for Health Predictions

This form represents the exact feature set used during ML model training.
It preserves the exact feature order and uses the same encoders for categorical features.

Critical constraints:
- Feature order must match training data exactly
- Categorical choices come from encoder.classes_ (values seen during training)
- Numeric fields accept raw values (will be scaled during prediction)
"""

from django import forms
from .ml_loader import ENCODER_CHOICES

# Model type choices
MODEL_CHOICES = [
    ('obesity', 'Obesity'),
    ('diabetes', 'Diabetes'),
]


def get_categorical_choices(feature_name):
    """
    Get valid choices for a categorical feature from loaded JSON.
    
    Args:
        feature_name: Name of the categorical feature
    
    Returns:
        list: List of tuples for ChoiceField choices
    """
    if feature_name in ENCODER_CHOICES:
        # Return list of tuples (value, display_name)
        return [(value, value) for value in ENCODER_CHOICES[feature_name]]
    return []


class HealthPredictionForm(forms.Form):
    """
    Unified form for health predictions (Obesity and Diabetes).
    
    This form includes all 15 features in the exact order used during training:
    1. Risk_Level (categorical)
    2-9. Numeric features
    10. StatusName (categorical)
    11-15. Numeric features
    
    Feature order must match the training feature order exactly.
    """
    
    # Model selection field
    model_type = forms.ChoiceField(
        choices=MODEL_CHOICES,
        label='Prediction Type',
        widget=forms.Select(attrs={
            'class': 'form-control',
            'aria-label': 'Select prediction type'
        }),
        help_text='Choose Obesity or Diabetes prediction'
    )
    
    # Categorical Feature 1: Risk_Level (first feature)
    Risk_Level = forms.ChoiceField(
        choices=[],
        label='Risk Level',
        widget=forms.Select(attrs={
            'class': 'form-control',
            'aria-required': 'true'
        }),
        help_text='Select risk level'
    )
    
    # Numeric Features (positions 2-9)
    VLFOODSEC_13_15 = forms.FloatField(
        label='Very Low Food Security (2013-2015)',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'placeholder': 'Enter VLFOODSEC 13-15 value',
            'aria-required': 'true'
        }),
        help_text='Very Low Food Security 2013-2015'
    )
    
    Adult_Obesity_Rate_08 = forms.FloatField(
        label='Adult Obesity Rate (2008)',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'placeholder': 'Enter adult obesity rate',
            'aria-required': 'true'
        }),
        help_text='Adult obesity rate in 2008'
    )
    
    CH_FOODINSEC_12_15 = forms.FloatField(
        label='Child Food Insecurity (2012-2015)',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'placeholder': 'Enter CH FOODINSEC 12-15 value',
            'aria-required': 'true'
        }),
        help_text='Child Food Insecurity 2012-2015'
    )
    
    Median_Income = forms.FloatField(
        label='Median Income',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'min': '0',
            'placeholder': 'Enter median income',
            'aria-required': 'true'
        }),
        help_text='Median income'
    )
    
    MILK_SODA_PRICE10 = forms.FloatField(
        label='Milk/Soda Price Ratio (2010)',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'min': '0',
            'placeholder': 'Enter milk/soda price ratio',
            'aria-required': 'true'
        }),
        help_text='Milk to soda price ratio in 2010'
    )
    
    Farmers_Markets_Count_16 = forms.FloatField(
        label='Farmers Markets Count (2016)',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '1',
            'min': '0',
            'placeholder': 'Enter farmers markets count',
            'aria-required': 'true'
        }),
        help_text='Number of farmers markets in 2016'
    )
    
    GYMs_Per_1000_Count_14 = forms.FloatField(
        label='Gyms per 1,000 (2014)',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'min': '0',
            'placeholder': 'Enter GYMs per 1000',
            'aria-required': 'true'
        }),
        help_text='Number of GYMs per 1000 people in 2014'
    )
    
    Adult_Diabetes_Rate_08 = forms.FloatField(
        label='Adult Diabetes Rate (2008)',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'placeholder': 'Enter adult diabetes rate',
            'aria-required': 'true'
        }),
        help_text='Adult diabetes rate in 2008'
    )
    
    # Categorical Feature 2: StatusName (position 10)
    StatusName = forms.ChoiceField(
        choices=[],
        label='Status Name',
        widget=forms.Select(attrs={
            'class': 'form-control',
            'aria-required': 'true'
        }),
        help_text='Select status'
    )
    
    # Numeric Features (positions 11-15)
    FSRPTH14 = forms.FloatField(
        label='Full-Service Restaurants/1,000 (2014)',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'placeholder': 'Enter FSRPTH14 value',
            'aria-required': 'true'
        }),
        help_text='FSRPTH14 metric'
    )
    
    Poverty_Rate = forms.FloatField(
        label='Poverty Rate',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'min': '0',
            'placeholder': 'Enter poverty rate',
            'aria-required': 'true'
        }),
        help_text='Poverty rate percentage'
    )
    
    VLFOODSEC_10_12 = forms.FloatField(
        label='Very Low Food Security (2010-2012)',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'placeholder': 'Enter VLFOODSEC 10-12 value',
            'aria-required': 'true'
        }),
        help_text='Very Low Food Security 2010-2012'
    )
    
    PCT_NHBLACK10 = forms.FloatField(
        label='% Non-Hispanic Black (2010)',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'min': '0',
            'placeholder': 'Enter percentage',
            'aria-required': 'true'
        }),
        help_text='Percentage Non-Hispanic Black in 2010'
    )
    
    PCH_VEG_ACRESPTH_07_12 = forms.FloatField(
        label='% Change Veg Acres/1,000 (2007-2012)',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'placeholder': 'Enter value',
            'aria-required': 'true'
        }),
        help_text='Percent change vegetable acres per thousand 2007-2012'
    )
    
    def __init__(self, *args, **kwargs):
        """
        Initialize form and populate categorical field choices from encoders.
        
        This must be done at initialization time to ensure encoder.classes_
        are available for dropdown population. We do NOT refit encoders.
        """
        super().__init__(*args, **kwargs)
        
        # Populate categorical field choices from encoders
        # Only Risk_Level and StatusName are categorical
        categorical_fields = ['Risk_Level', 'StatusName']
        
        for field_name in categorical_fields:
            if field_name in self.fields:
                choices = get_categorical_choices(field_name)
                self.fields[field_name].choices = choices
                
                # Set default to first choice if available
                if choices and not self.fields[field_name].initial:
                    self.fields[field_name].initial = choices[0][0]


class ClusteringForm(forms.Form):
    """
    Form for Clustering Prediction (K-Means).
    """
    Adult_Diabetes_Rate_08 = forms.FloatField(
        label='Adult Diabetes Rate (2008)',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Rate'}),
        required=True
    )
    Adult_Diabetes_Rate13 = forms.FloatField(
        label='Adult Diabetes Rate (2013)',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Rate'}),
        required=True
    )
    Adult_Obesity_Rate_08 = forms.FloatField(
        label='Adult Obesity Rate (2008)',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Rate'}),
        required=True
    )
    Adult_Obesity_Rate13 = forms.FloatField(
        label='Adult Obesity Rate (2013)',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Rate'}),
        required=True
    )
    GYMs_Per_1000_Count_14 = forms.FloatField(
        label='Gyms per 1,000 (2014)',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.001', 'placeholder': 'Count'}),
        required=True
    )
    Farmers_Markets_Count_16 = forms.FloatField(
        label='Farmers Markets Count (2016)',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '1', 'placeholder': 'Count'}),
        required=True
    )
    GROCPTH09 = forms.FloatField(
        label='Grocery Stores Per 1000 (2009)',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.001', 'placeholder': 'Count'}),
        required=True
    )

