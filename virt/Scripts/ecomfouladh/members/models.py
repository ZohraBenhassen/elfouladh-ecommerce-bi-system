from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    USER_ROLES = [
        ('admin', 'Admin'),
        ('sdvente', 'Sales'),
        ('dirgen', 'Director General'),
        ('livreur', 'Delivery'),
        
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='members_profile')
    role = models.CharField(max_length=10, choices=USER_ROLES)

    def __str__(self):
        return self.user.username
