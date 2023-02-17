from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .helper import cleanText, similaritySearch
from .models import Question,QuestionCountHistory
from .serializers import QuestionSerializer
from django.http import HttpResponse

from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework.authtoken.models import Token
from accounts.models import CustomUser

from datetime import date

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
@authentication_classes([TokenAuthentication])
def queryQuestion(request):
    if request.method == 'POST':
        queryQuestion = request.data['queryQuestion']
        ques = cleanText(queryQuestion)
        token_key = request.auth
        token = Token.objects.get(key=token_key)
        user = token.user
        history=None
        try:
            history=QuestionCountHistory.objects.get(user=user,date=date.today())   
        except QuestionCountHistory.DoesNotExist:
            history=QuestionCountHistory.objects.create(user=user,date=date.today())
        # print("---------------",history)
        history.count+=1
        history.save()
        similarQuesId = similaritySearch(ques)
        similarQuesId = similarQuesId+10043
        similarLst = [Question.objects.get(pk=i) for i in similarQuesId]
        serializeQuestion = QuestionSerializer(similarLst, many=True)
        return Response(serializeQuestion.data)

# @api_view(['POST'])
# def uploadDocument(request):
#     if request.method == "POST":
#         author = request.data.get("author")
#         date = request.data.get("date")
#         documentId=request.data.get("documentId")
#         note= request.data.get("note")
#         sentences=request.data.get("sentences")
#         model_instance =UploadDocument.objects.create(author=author,date=date,documentId=documentId,note=note)
#         for sentence in sentences:
#             DocumentQuestions.objects.create(question=sentence,documentId=model_instance)
        
#     return render(request, 'bertConnector/indexApi.html')


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def apiTest(request):
    return Response({"message":"visible"})

def index(request):
    return render(request, 'bertConnector/indexApi.html')
