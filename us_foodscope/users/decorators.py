from functools import wraps
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Define role-based access permissions for each prediction section
ROLE_PERMISSIONS = {
    'access': ['ADMIN', 'ACCESS_INSECURITY_MANAGER'],
    'insecurity': ['ADMIN', 'ACCESS_INSECURITY_MANAGER'],
    'health': ['ADMIN', 'HEALTH_MANAGER'],
    'finance': ['ADMIN', 'FINANCE_MANAGER'],
    'local': ['ADMIN', 'LOCAL_ENVIRONMENT_MANAGER'],
    'food_env': ['ADMIN', 'LOCAL_ENVIRONMENT_MANAGER'],
}


def role_required(allowed_roles):
    """
    Decorator to restrict access to views based on user roles.
    
    Usage:
        @role_required(['ADMIN', 'HEALTH_MANAGER'])
        def my_view(request):
            ...
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapped_view(request, *args, **kwargs):
            user = request.user
            if not hasattr(user, 'role'):
                return render(request, 'users/access_denied.html', {
                    'message': 'User role not found.'
                }, status=403)
            
            if user.role in allowed_roles or user.is_admin():
                return view_func(request, *args, **kwargs)
            else:
                return render(request, 'users/access_denied.html', {
                    'user': user,
                    'message': f'Your role ({user.get_role_display()}) does not have permission to access this page.'
                }, status=403)
        return wrapped_view
    return decorator


def prediction_access_required(section_name):
    """
    Decorator to restrict access to prediction views based on role permissions.
    
    Usage:
        @prediction_access_required('health')
        def health_view(request):
            ...
    """
    allowed_roles = ROLE_PERMISSIONS.get(section_name, ['ADMIN'])
    return role_required(allowed_roles)

