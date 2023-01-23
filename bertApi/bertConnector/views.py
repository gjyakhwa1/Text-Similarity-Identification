from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .helper import cleanText, similaritySearch
from .models import Question,UploadDocument,DocumentQuestions
from .serializers import QuestionSerializer
from django.http import HttpResponse


# Create your views here.


@api_view(['GET'])
def viewQuestion(request):
    questions = Question.objects.all()
    serializeQuestion = QuestionSerializer(questions, many=True)
    return Response(serializeQuestion.data)

@api_view(['GET'])
def test(request):
    return HttpResponse("connected",status=200)

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

@api_view(['POST'])
def uploadDocument(request):
    if request.method == "POST":
        author = request.data.get("author")
        date = request.data.get("date")
        documentId=request.data.get("documentId")
        note= request.data.get("note")
        sentences=request.data.get("sentences")
        model_instance =UploadDocument.objects.create(author=author,date=date,documentId=documentId,note=note)
        for sentence in sentences:
            DocumentQuestions.objects.create(question=sentence,documentId=model_instance)
        
    return render(request, 'bertConnector/indexApi.html')

def index(request):
    return render(request, 'bertConnector/indexApi.html')
