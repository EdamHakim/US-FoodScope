from django import forms


# -------------------------
# ✅ PREDICTION FORM (10 features)
# -------------------------
from django import forms

class AccessPredictionForm(forms.Form):
    PCT_LACCESS_POP10 = forms.FloatField(label="Percent Low Access Population (2010)")
    LACCESS_LOWI15 = forms.FloatField(label="Low Income Low Access (2015)")
    LACCESS_HISP15 = forms.FloatField(label="Hispanic Low Access (2015)")
    LACCESS_NHASIAN15 = forms.FloatField(label="Non-Hispanic Asian Low Access (2015)")
    LACCESS_BLACK15 = forms.FloatField(label="Black Low Access (2015)")
    Median_Income = forms.FloatField(label="Median Income")
    Poverty_Rate = forms.FloatField(label="Poverty Rate")
    Food_Tax_Rate_14 = forms.FloatField(label="Food Tax Rate (2014)")
    PCT_65OLDER10 = forms.FloatField(label="Percent Age 65+ (2010)")
    PCT_18YOUNGER10 = forms.FloatField(label="Percent Age ≤18 (2010)")



# -------------------------
# ✅ CLUSTERING FORM (9 features)
# -------------------------
class AccessClusteringForm(forms.Form):
    Poverty_Rate = forms.FloatField(label="Poverty Rate", required=True)
    Median_Income = forms.FloatField(label="Median Income", required=True)
    PCT_65OLDER10 = forms.FloatField(label="Percent Age 65+ (2010)", required=True)
    PCT_18YOUNGER10 = forms.FloatField(label="Percent Age ≤18 (2010)", required=True)
    POPLOSS10 = forms.FloatField(label="Population Loss (2010)", required=True)
    LACCESS_HISP15 = forms.FloatField(label="Hispanic Low Access (2015)", required=True)
    LACCESS_NHASIAN15 = forms.FloatField(label="Non-Hispanic Asian Low Access (2015)", required=True)
    LACCESS_BLACK15 = forms.FloatField(label="Black Low Access (2015)", required=True)
    PCT_LACCESS_POP10 = forms.FloatField(label="Percent Low Access Population (2010)", required=True)
