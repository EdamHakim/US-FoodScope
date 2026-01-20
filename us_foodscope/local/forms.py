"""
Django Form for Local Food Regression Prediction

Form for clustering and regression analysis of local food characteristics.
"""

from django import forms
from .ml_loader import CLUSTERING_FEATURES
from collections import OrderedDict


# Numeric fields for regression input
class LocalRegressionForm(forms.Form):
    """
    Form for local food regression and clustering prediction.
    
    Features are loaded dynamically from clustering_features.json
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Dynamically add fields based on clustering features
        if CLUSTERING_FEATURES:
            for feature_name, feature_info in CLUSTERING_FEATURES.items():
                feature_type = feature_info.get('type', 'numeric')
                label = feature_info.get('label', feature_name.replace('_', ' ').title())
                help_text = feature_info.get('description', '')
                
                if feature_type == 'numeric':
                    # Create numeric field with min/max from feature info
                    min_value = feature_info.get('min', None)
                    max_value = feature_info.get('max', None)
                    
                    # Build widget attributes
                    widget_attrs = {
                        'class': 'form-control',
                        'placeholder': f'Enter {label}',
                        'step': '0.01'
                    }
                    
                    # Add min/max HTML attributes for client-side validation
                    if min_value is not None:
                        widget_attrs['min'] = str(min_value)
                    if max_value is not None:
                        widget_attrs['max'] = str(max_value)
                    
                    self.fields[feature_name] = forms.FloatField(
                        label=label,
                        help_text=help_text,
                        required=True,
                        min_value=min_value,
                        max_value=max_value,
                        widget=forms.NumberInput(attrs=widget_attrs)
                    )
                    
                elif feature_type == 'categorical':
                    # Create choice field
                    choices = [(v, v) for v in feature_info.get('categories', [])]
                    self.fields[feature_name] = forms.ChoiceField(
                        label=label,
                        help_text=help_text,
                        choices=[('', 'Select an option')] + choices,
                        required=True,
                        widget=forms.Select(attrs={
                            'class': 'form-control'
                        })
                    )
        else:
            # Fallback if no features loaded
            self.fields['feature_input'] = forms.CharField(
                label='Input Features',
                help_text='Features not loaded from configuration',
                widget=forms.Textarea(attrs={
                    'class': 'form-control',
                    'rows': 5,
                    'placeholder': 'Features configuration missing'
                })
            )

    def get_field_groups(self):
        """Return BoundFields grouped by category for template rendering"""
        field_groups = OrderedDict()
        
        # Define category order
        category_order = {
            'Economic': 0,
            'Demographics': 1,
            'Ethnicity': 2,
            'Food Security': 3,
            'Local Food Access': 4,
            'Local Agriculture': 5,
        }
        
        # Group field names by category
        temp_groups = {}
        for field_name in self.fields.keys():
            if field_name == 'csrf_token':
                continue
            
            # Get category from CLUSTERING_FEATURES
            feature_info = CLUSTERING_FEATURES.get(field_name, {})
            category = feature_info.get('category', 'Other')
            
            if category not in temp_groups:
                temp_groups[category] = []
            
            temp_groups[category].append(field_name)
        
        # Sort categories by predefined order and convert field names to BoundFields
        sorted_categories = sorted(
            temp_groups.items(),
            key=lambda x: category_order.get(x[0], 999)
        )
        
        for category, field_names in sorted_categories:
            # Convert field names to BoundFields
            field_groups[category] = [self[field_name] for field_name in field_names]
        
        return field_groups

