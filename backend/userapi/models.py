from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    SYSTEM_ADMIN = 'System Admin'
    STS_MANAGER = 'STS Manager'
    LANDFILL_MANAGER = 'Landfill Manager'
    UNASSIGNED = 'Unassigned'
    ROLE_CHOICES = [
        (SYSTEM_ADMIN, 'System Admin'),
        (STS_MANAGER, 'STS Manager'),
        (LANDFILL_MANAGER, 'Landfill Manager'),
        (UNASSIGNED, 'Unassigned'),
    ]
    role = models.CharField(max_length=100, choices=ROLE_CHOICES)