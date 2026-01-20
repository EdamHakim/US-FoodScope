from django import forms


class FinancePredictionForm(forms.Form):
    """
    Finance Prediction Form
    Handles both Tax Rate predictions and Clustering inputs
    """
    
    # ============================================
    # HIDDEN FIELD - Model Type
    # ============================================
    model_type = forms.CharField(
        widget=forms.HiddenInput(),
        required=False,
        initial='tax_rate'
    )
    
    # ============================================
    # TAX RATE PREDICTION FIELDS
    # ============================================
    
    Adult_Obesity_Rate_08 = forms.FloatField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter rate (e.g., 25.5)',
            'step': '0.1',
            'min': '0',
            'max': '100'
        }),
        label='Adult Obesity Rate 2008'
    )
    
    Adult_Diabetes_Rate_08 = forms.FloatField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter rate (e.g., 10.2)',
            'step': '0.1',
            'min': '0',
            'max': '100'
        }),
        label='Adult Diabetes Rate 2008'
    )
    
    Adult_Obesity_Rate13 = forms.FloatField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter rate (e.g., 28.3)',
            'step': '0.1',
            'min': '0',
            'max': '100'
        }),
        label='Adult Obesity Rate 2013'
    )
    
    Adult_Diabetes_Rate13 = forms.FloatField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter rate (e.g., 11.5)',
            'step': '0.1',
            'min': '0',
            'max': '100'
        }),
        label='Adult Diabetes Rate 2013'
    )
    
    SODATAX_STORES14 = forms.FloatField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter value (e.g., 150)',
            'step': '0.1',
            'min': '0'
        }),
        label='Soda Tax Stores 2014'
    )
    
    CHIPSTAX_VENDM14 = forms.FloatField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter value (e.g., 75)',
            'step': '0.1',
            'min': '0'
        }),
        label='Chips Tax Vending 2014'
    )
    
    PCT_LOCLFARM12 = forms.FloatField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter percentage (e.g., 15.5)',
            'step': '0.1',
            'min': '0',
            'max': '100'
        }),
        label='Percent Local Farms 2012'
    )
    
    VLFOODSEC_10_12 = forms.FloatField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter value (e.g., 5.2)',
            'step': '0.1',
            'min': '0'
        }),
        label='Very Low Food Security 2010-12'
    )
    
    # ============================================
    # CLUSTERING FIELDS
    # ============================================
    
    Median_Income = forms.FloatField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter median income (e.g., 55000)',
            'step': '1',
            'min': '0'
        }),
        label='Median Income'
    )
    
    FOODINSEC_13_15 = forms.FloatField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter value (e.g., 12.5)',
            'step': '0.1',
            'min': '0',
            'max': '100'
        }),
        label='Food Insecurity 2013-15'
    )
    
    # ============================================
    # CUSTOM VALIDATION
    # ============================================
    
    def clean(self):
        """
        Custom validation to ensure required fields are filled based on model_type
        """
        cleaned_data = super().clean()
        model_type = cleaned_data.get('model_type', 'tax_rate')
        
        print(f"[FORM VALIDATION] Model type: {model_type}")
        
        if model_type == 'tax_rate':
            # Validate tax rate prediction fields
            required_fields = [
                'Adult_Obesity_Rate_08',
                'Adult_Diabetes_Rate_08',
                'Adult_Obesity_Rate13',
                'Adult_Diabetes_Rate13',
                'SODATAX_STORES14',
                'CHIPSTAX_VENDM14',
                'PCT_LOCLFARM12',
                'VLFOODSEC_10_12'
            ]
            
            missing_fields = []
            for field in required_fields:
                value = cleaned_data.get(field)
                if value is None or value == '':
                    missing_fields.append(field)
                    self.add_error(field, 'This field is required for tax rate predictions.')
            
            if missing_fields:
                print(f"[FORM VALIDATION] Missing tax rate fields: {missing_fields}")
            else:
                print(f"[FORM VALIDATION] All tax rate fields present")
        
        elif model_type == 'clustering':
            # Validate clustering fields
            required_fields = [
                'Median_Income',
                'FOODINSEC_13_15',
                'Adult_Obesity_Rate13'
            ]
            
            missing_fields = []
            for field in required_fields:
                value = cleaned_data.get(field)
                if value is None or value == '':
                    missing_fields.append(field)
                    self.add_error(field, 'This field is required for clustering.')
            
            if missing_fields:
                print(f"[FORM VALIDATION] Missing clustering fields: {missing_fields}")
            else:
                print(f"[FORM VALIDATION] All clustering fields present")
        
        else:
            print(f"[FORM VALIDATION] Unknown model type: {model_type}")
        
        return cleaned_data
    
    def clean_Adult_Obesity_Rate_08(self):
        """Validate Adult Obesity Rate 2008"""
        value = self.cleaned_data.get('Adult_Obesity_Rate_08')
        if value is not None and (value < 0 or value > 100):
            raise forms.ValidationError('Rate must be between 0 and 100')
        return value
    
    def clean_Adult_Diabetes_Rate_08(self):
        """Validate Adult Diabetes Rate 2008"""
        value = self.cleaned_data.get('Adult_Diabetes_Rate_08')
        if value is not None and (value < 0 or value > 100):
            raise forms.ValidationError('Rate must be between 0 and 100')
        return value
    
    def clean_Adult_Obesity_Rate13(self):
        """Validate Adult Obesity Rate 2013"""
        value = self.cleaned_data.get('Adult_Obesity_Rate13')
        if value is not None and (value < 0 or value > 100):
            raise forms.ValidationError('Rate must be between 0 and 100')
        return value
    
    def clean_Adult_Diabetes_Rate13(self):
        """Validate Adult Diabetes Rate 2013"""
        value = self.cleaned_data.get('Adult_Diabetes_Rate13')
        if value is not None and (value < 0 or value > 100):
            raise forms.ValidationError('Rate must be between 0 and 100')
        return value
    
    def clean_PCT_LOCLFARM12(self):
        """Validate Percent Local Farms 2012"""
        value = self.cleaned_data.get('PCT_LOCLFARM12')
        if value is not None and (value < 0 or value > 100):
            raise forms.ValidationError('Percentage must be between 0 and 100')
        return value
    
    def clean_FOODINSEC_13_15(self):
        """Validate Food Insecurity 2013-15"""
        value = self.cleaned_data.get('FOODINSEC_13_15')
        if value is not None and (value < 0 or value > 100):
            raise forms.ValidationError('Value must be between 0 and 100')
        return value
    
    def clean_Median_Income(self):
        """Validate Median Income"""
        value = self.cleaned_data.get('Median_Income')
        if value is not None and value < 0:
            raise forms.ValidationError('Median income cannot be negative')
        return value
    
    def clean_SODATAX_STORES14(self):
        """Validate Soda Tax Stores 2014"""
        value = self.cleaned_data.get('SODATAX_STORES14')
        if value is not None and value < 0:
            raise forms.ValidationError('Value cannot be negative')
        return value
    
    def clean_CHIPSTAX_VENDM14(self):
        """Validate Chips Tax Vending 2014"""
        value = self.cleaned_data.get('CHIPSTAX_VENDM14')
        if value is not None and value < 0:
            raise forms.ValidationError('Value cannot be negative')
        return value
    
    def clean_VLFOODSEC_10_12(self):
        """Validate Very Low Food Security 2010-12"""
        value = self.cleaned_data.get('VLFOODSEC_10_12')
        if value is not None and value < 0:
            raise forms.ValidationError('Value cannot be negative')
        return value