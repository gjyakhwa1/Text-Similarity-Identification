from django.contrib.auth.models import AbstractUser,Group,Permission
from django.db import models

class CustomUser(AbstractUser):
    is_approved = models.BooleanField(default=False)

class LoginHistory(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    login_at=models.DateTimeField(auto_now_add=True)
    logout_at=models.DateTimeField(null=True,blank=True)
    
    def __str__(self):
        return self.user.username
