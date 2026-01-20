from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    """Custom user model with roles and additional fields"""
    
    ROLE_CHOICES = [
        ('ADMIN', 'Admin'),
        ('ACCESS_INSECURITY_MANAGER', 'Access Insecurity Manager'),
        ('HEALTH_MANAGER', 'Health Manager'),
        ('FINANCE_MANAGER', 'Finance Manager'),
        ('LOCAL_ENVIRONMENT_MANAGER', 'Local Environment Manager'),
    ]
    
    role = models.CharField(
        max_length=30,
        choices=ROLE_CHOICES,
        help_text='User role determines access permissions'
    )
    
    profile_image = models.FileField(
        upload_to='profile_images/',
        blank=True,
        null=True,
        help_text='Optional profile picture'
    )
    
    email = models.EmailField(unique=True, blank=False)
    
    first_name = models.CharField(max_length=150, blank=False)
    last_name = models.CharField(max_length=150, blank=False)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()})"
    
    def is_admin(self):
        """Check if user is an admin"""
        return self.role == 'ADMIN'
    
    def is_access_insecurity_manager(self):
        """Check if user is an access insecurity manager"""
        return self.role == 'ACCESS_INSECURITY_MANAGER'
    
    def is_health_manager(self):
        """Check if user is a health manager"""
        return self.role == 'HEALTH_MANAGER'
    
    def is_finance_manager(self):
        """Check if user is a finance manager"""
        return self.role == 'FINANCE_MANAGER'
    
    def is_local_environment_manager(self):
        """Check if user is a local environment manager"""
        return self.role == 'LOCAL_ENVIRONMENT_MANAGER'
    
    def can_access_section(self, section_name):
        """Check if user has permission to access a specific prediction section"""
        # Admin has access to all sections
        if self.is_admin():
            return True
        
        # Define role-based access permissions
        role_permissions = {
            'access': ['ACCESS_INSECURITY_MANAGER'],
            'insecurity': ['ACCESS_INSECURITY_MANAGER'],
            'health': ['HEALTH_MANAGER'],
            'finance': ['FINANCE_MANAGER'],
            'local': ['LOCAL_ENVIRONMENT_MANAGER'],
            'food_env': ['LOCAL_ENVIRONMENT_MANAGER'],
        }
        
        allowed_roles = role_permissions.get(section_name, [])
        return self.role in allowed_roles
    
    @property
    def can_access_access(self):
        """Check if user can access the access prediction section"""
        return self.can_access_section('access')
    
    @property
    def can_access_insecurity(self):
        """Check if user can access the insecurity prediction section"""
        return self.can_access_section('insecurity')
    
    @property
    def can_access_health(self):
        """Check if user can access the health prediction section"""
        return self.can_access_section('health')
    
    @property
    def can_access_finance(self):
        """Check if user can access the finance prediction section"""
        return self.can_access_section('finance')
    
    @property
    def can_access_local(self):
        """Check if user can access the local prediction section"""
        return self.can_access_section('local')
    
    @property
    def can_access_food_env(self):
        """Check if user can access the food environment prediction section"""
        return self.can_access_section('food_env')