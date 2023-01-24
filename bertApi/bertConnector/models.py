from django.db import models

# Create your models here.


class Question(models.Model):
    question = models.TextField()

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.question
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
