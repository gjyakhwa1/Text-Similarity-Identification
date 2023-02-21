from django.db import models
from accounts.models import CustomUser
# Create your models here.


class Question(models.Model):
    question = models.TextField()

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.question

class QuestionCountHistory(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    date=models.DateField()
    count=models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.user.username

# class UploadDocument(models.Model):
#     author = models.CharField(blank=False,max_length=100)
#     date = models.DateField(blank=False)
#     documentId = models.CharField(blank=False,unique=True,max_length=100)
#     note =models.CharField(blank=True,max_length=100)
#     class Meta:
#         ordering=['id']
        
#     def __str__(self):
#         return self.documentId

# class DocumentQuestions(models.Model):
#     question = models.TextField()
#     documentId = models.ForeignKey(UploadDocument,to_field="documentId",on_delete=models.CASCADE)
#     class Meta:
#         ordering =['id']
    
#     def __str__(self):
#         return self.question
