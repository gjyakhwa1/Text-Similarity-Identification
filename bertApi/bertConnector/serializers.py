from .models import Question,QuestionCountHistory
from rest_framework import serializers


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'

class QuestionCountHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model =QuestionCountHistory
        fields="__all__"

