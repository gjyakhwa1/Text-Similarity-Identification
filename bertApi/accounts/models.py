from django.contrib.auth.models import AbstractUser,Group,Permission
from django.db import models

class CustomUser(AbstractUser):
    APPROVAL_CHOICES = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    )
    approvalStatus = models.CharField(default="Pending",max_length=15,choices=APPROVAL_CHOICES)
    totalQueryQuestion = models.IntegerField(default=0)
    openAIToken= models.CharField(blank=True,max_length=50,default="")

class LoginHistory(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    login_at=models.DateTimeField(auto_now_add=True)
    logout_at=models.DateTimeField(null=True,blank=True)
    
    def __str__(self):
        return self.user.username
