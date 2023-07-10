from .models import Question,QuestionCountHistory, ServerStatus
from rest_framework import serializers
from accounts.serializers import CustomUserSerializer


class QuestionSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    class Meta:
        model = Question
        # fields = '__all__'
        fields=['user','id','question','date','examYear','examinationType','date']

class QuestionCountHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model =QuestionCountHistory
        fields="__all__"
    
class ServerStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model =ServerStatus
        fields="__all__"

