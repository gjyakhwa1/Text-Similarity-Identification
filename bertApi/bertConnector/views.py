from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .helper import cleanText, similaritySearch
from .models import Question
from .serializers import QuestionSerializer


# Create your views here.


@api_view(['GET'])
def viewQuestion(request):
    questions = Question.objects.all()
    serializeQuestion = QuestionSerializer(questions, many=True)
    return Response(serializeQuestion.data)


@api_view(['POST'])
def queryQuestion(request):
    if request.method == 'POST':
        queryQuestion = request.data['queryQuestion']
        ques = cleanText(queryQuestion)
        similarQuesId = similaritySearch(ques)
        similarQuesId = similarQuesId+1
        similarLst = [Question.objects.get(pk=i) for i in similarQuesId]
        serializeQuestion = QuestionSerializer(similarLst, many=True)
        return Response(serializeQuestion.data)


def index(request):
    return render(request, 'bertConnector/indexApi.html')
