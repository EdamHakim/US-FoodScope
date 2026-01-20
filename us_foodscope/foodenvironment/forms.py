"""
Django Form for Food Environment Predictions

This form represents the exact feature set used during ML model training.
It preserves the exact feature order for grocery store density prediction.

Critical constraints:
- Feature order must match training data exactly
- RestaurantCategory_ID is categorical (1 or 2)
- All other fields are numeric values
- Features are sent raw to the API (scaling happens on HF Space)
"""

from django import forms


class FoodEnvironmentPredictionForm(forms.Form):
    """
    Form for food environment analysis and grocery store density prediction.
    
    This form includes all 9 features in the exact order used during training:
    2. Soda Price 2010
    3. Farmers Market Path
    4. Grocery Store Path 2009
    5. Change in Grocery Path 2009-2014
    6. Fast Food Restaurant Path 2009
    7. Fast Food Restaurant Path 2014
    8. Population 65+ Years Old
    9. Population Loss
    
    Feature order must match the training feature order exactly.
    """
    
    
    # Numeric Feature 1: Soda Price
    soda_price = forms.FloatField(
        label='Soda Price (cents)',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'min': '0',
            'placeholder': 'Enter soda price in cents',
            'aria-required': 'true',
        }),
        help_text='Average soda price in cents (2010)',
        required=True
    )
    
    # Numeric Feature 2: Farmers Market Path
    fmrktpth16 = forms.FloatField(
        label='Farmers Market Path (%)',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'min': '0',
            'max': '100',
            'placeholder': 'Enter percentage',
            'aria-required': 'true',
        }),
        help_text='Percentage of population with access to farmers market',
        required=True
    )
    
    # Numeric Feature 3: Grocery Store Path 2009
    grocpth09 = forms.FloatField(
        label='Grocery Store Path 2009 (%)',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'min': '0',
            'max': '100',
            'placeholder': 'Enter percentage',
            'aria-required': 'true',
        }),
        help_text='Percentage of population with access to grocery stores in 2009',
        required=True
    )
    
    # Numeric Feature 4: Change in Grocery Path
    pch_grocpth_09_14 = forms.FloatField(
        label='Change in Grocery Path 2009-2014 (%)',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'placeholder': 'Enter percentage change',
            'aria-required': 'true',
        }),
        help_text='Percentage change in grocery store access from 2009 to 2014',
        required=True
    )
    
    # Numeric Feature 5: Fast Food Restaurant Path 2009
    fsrpth09 = forms.FloatField(
        label='Fast Food Restaurant Path 2009 (%)',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'min': '0',
            'max': '100',
            'placeholder': 'Enter percentage',
            'aria-required': 'true',
        }),
        help_text='Percentage of population with access to fast food in 2009',
        required=True
    )
    
    # Numeric Feature 6: Fast Food Restaurant Path 2014
    fsrpth14 = forms.FloatField(
        label='Fast Food Restaurant Path 2014 (%)',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'min': '0',
            'max': '100',
            'placeholder': 'Enter percentage',
            'aria-required': 'true',
        }),
        help_text='Percentage of population with access to fast food in 2014',
        required=True
    )
    
    # Numeric Feature 7: Population 65+ Years Old
    pct_65older10 = forms.FloatField(
        label='Population 65+ Years Old (%)',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'min': '0',
            'max': '100',
            'placeholder': 'Enter percentage',
            'aria-required': 'true',
        }),
        help_text='Percentage of population aged 65 and older in 2010',
        required=True
    )
    
    # Numeric Feature 8: Population Loss
    poploss10 = forms.FloatField(
        label='Population Loss (%)',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'placeholder': 'Enter percentage loss',
            'aria-required': 'true',
        }),
        help_text='Percentage of population loss from 2000 to 2010',
        required=True
    )
    
    def clean(self):
        """
        Perform form-level validation.
        
        Checks that all required fields are provided and have valid values.
        """
        cleaned_data = super().clean()
        
        
        # Validate percentage fields are between 0 and 100 (if provided)
        percentage_fields = [
            'fmrktpth16', 'fsrpth09', 
            'fsrpth14', 'pct_65older10'
        ]
        
        for field_name in percentage_fields:
            value = cleaned_data.get(field_name)
            if value is not None and (value < 0 or value > 100):
                self.add_error(field_name, 
                             f'{field_name} must be between 0 and 100')
        
        return cleaned_data