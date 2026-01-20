from django import forms

class FoodInsecurityPredictionForm(forms.Form):
    """
    Form for food insecurity prediction.
    Collects all features needed for the RandomForest model.
    """
    
    # Features in the order they were used for training
    PCT_LACCESS_POP15 = forms.FloatField(
        label='Low Access Population %',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'placeholder': 'Percentage of low food access population',
            'aria-required': 'true'
        }),
        help_text='Percentage of population with low food access'
    )
    
    LACCESS_BLACK15 = forms.FloatField(
        label='Black Low Access Population',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'placeholder': 'Count of Black population with low access',
            'aria-required': 'true'
        }),
        help_text='Number of Black population with low food access'
    )
    
    LACCESS_HISP15 = forms.FloatField(
        label='Hispanic Low Access Population',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'placeholder': 'Count of Hispanic population with low access',
            'aria-required': 'true'
        }),
        help_text='Number of Hispanic population with low food access'
    )
    
    LACCESS_NHASIAN15 = forms.FloatField(
        label='Asian Low Access Population',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'placeholder': 'Count of Asian population with low access',
            'aria-required': 'true'
        }),
        help_text='Number of Asian population with low food access'
    )
    
    Poverty_Rate = forms.FloatField(
        label='Poverty Rate %',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'placeholder': 'Percentage in poverty',
            'aria-required': 'true'
        }),
        help_text='Percentage of population below poverty line'
    )
    
    Adult_Obesity_Rate13 = forms.FloatField(
        label='Adult Obesity Rate %',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'placeholder': 'Adult obesity percentage',
            'aria-required': 'true'
        }),
        help_text='Adult obesity rate (2013 data)'
    )
    
    Adult_Diabetes_Rate13 = forms.FloatField(
        label='Adult Diabetes Rate %',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'placeholder': 'Adult diabetes percentage',
            'aria-required': 'true'
        }),
        help_text='Adult diabetes rate (2013 data)'
    )
    
    FOODINSEC_13_15 = forms.FloatField(
        label='Food Insecurity Index',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'placeholder': 'Food insecurity index value',
            'aria-required': 'true'
        }),
        help_text='Food insecurity index (2013-2015 data)'
    )
