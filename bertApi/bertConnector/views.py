from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse

from .helper import cleanText, similaritySearch, getCosineSimilarity, getCount
from .models import Question
from .serializers import QuestionSerializer


# Create your views here.


@api_view(['GET'])
def viewQuestion(request):
    questions = Question.objects.all()
    serializeQuestion = QuestionSerializer(questions, many=True)
    return Response(serializeQuestion.data)

@api_view(['GET'])
def test(request):
    return HttpResponse("ok")

@api_view(['POST'])
def queryQuestion(request):
    if request.method == 'POST':
        queryQuestion = request.data['queryQuestion']
        ques = cleanText(queryQuestion)
        similarQuesId = similaritySearch(ques)
        similarQuesId = similarQuesId+1
        similarLst = [Question.objects.get(pk=i) for i in similarQuesId]
        serializeQuestion = QuestionSerializer(similarLst, many=True)
        jsonRes = []
        for item in serializeQuestion.data:
            result= dict(item).get('question')
            jsonRes.append({"question": result, "similarity": getCosineSimilarity(ques, cleanText(result))})
        return Response(jsonRes)


def index(request):
    return render(request, 'bertConnector/indexApi.html')
