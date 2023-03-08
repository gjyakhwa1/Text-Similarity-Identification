from .models import Question,QuestionCountHistory, ServerStatus
from rest_framework import serializers


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'

class QuestionCountHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model =QuestionCountHistory
        fields="__all__"
    
class ServerStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model =ServerStatus
        fields="__all__"

