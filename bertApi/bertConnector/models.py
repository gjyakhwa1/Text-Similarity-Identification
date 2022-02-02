from django.db import models

# Create your models here.


class Question(models.Model):
    question = models.TextField()

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.question
