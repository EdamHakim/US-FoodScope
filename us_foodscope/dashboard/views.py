from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def dashboard_view(request):
    user = request.user
    role = user.role
    
    iframe_urls = {
        'ADMIN': 'https://app.powerbi.com/reportEmbed?reportId=4562eb1f-6168-4f87-acc0-3a57273cde06&autoAuth=true&ctid=604f1a96-cbe8-43f8-abbf-f8eaf5d85730',
        'ACCESS_INSECURITY_MANAGER': 'https://app.powerbi.com/reportEmbed?reportId=026ea629-39c4-4730-88e6-f66374a74efb&autoAuth=true&ctid=604f1a96-cbe8-43f8-abbf-f8eaf5d85730',
        'HEALTH_MANAGER': 'https://app.powerbi.com/reportEmbed?reportId=0b16b581-157b-4099-977e-60b660cd847a&autoAuth=true&ctid=604f1a96-cbe8-43f8-abbf-f8eaf5d85730',
        'FINANCE_MANAGER': 'https://app.powerbi.com/reportEmbed?reportId=0ca0c787-6379-472b-8b9d-52a8b72307e3&autoAuth=true&ctid=604f1a96-cbe8-43f8-abbf-f8eaf5d85730',
        'LOCAL_ENVIRONMENT_MANAGER': 'https://app.powerbi.com/reportEmbed?reportId=199f11f5-cd64-4c3b-810b-b4c956b82ea4&autoAuth=true&ctid=604f1a96-cbe8-43f8-abbf-f8eaf5d85730',
    }
    iframe_url = iframe_urls.get(role)
    context = {
        'iframe_url': iframe_url,
        'has_permission': iframe_url is not None
    }

    return render(request, 'dashboard/dashboard.html', context)
