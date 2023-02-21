from django.shortcuts import render
from django.http import HttpResponse

from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token

from accounts.helper import getWeeklyQueryData
from accounts.helper import getHighestQueryUsers
from .helper import cleanText, similaritySearch, switchAlgorithm
from .models import Question, QuestionCountHistory
from .serializers import QuestionSerializer

from datetime import date

# Create your views here.


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
def viewQuestion(request):
    questions = Question.objects.all()
    serializeQuestion = QuestionSerializer(questions, many=True)
    return Response(serializeQuestion.data)


@api_view(["GET"])
def test(request):
    return HttpResponse("connected", status=200)


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
def queryQuestion(request):
    global model, vectorIndex
    if request.method == "POST":
        queryQuestion = request.data["queryQuestion"]
        ques = cleanText(queryQuestion)
        token_key = request.auth
        token = Token.objects.get(key=token_key)
        user = token.user
        user.totalQueryQuestion += 1
        user.save()
        history = None
        try:
            history = QuestionCountHistory.objects.get(user=user, date=date.today())
        except QuestionCountHistory.DoesNotExist:
            history = QuestionCountHistory.objects.create(user=user, date=date.today())
        history.count += 1
        history.save()
        similarQuesId = similaritySearch(ques)
        similarQuesId = similarQuesId + 10043
        similarLst = [Question.objects.get(pk=i) for i in similarQuesId]
        serializeQuestion = QuestionSerializer(similarLst, many=True)
        return Response(serializeQuestion.data)


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
def highestQueryCountUsers(request):
    if request.method == "GET":
        data = getHighestQueryUsers()
        return Response(data)


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
def perDayQueryCount(request, user_id):
    if request.method == "GET":
        result = QuestionCountHistory.objects.filter(user= user_id).values('date','count')
        date = [ item['date'] for item in result]
        count = [item['count'] for item in result]
        return Response({"date":date,"count":count})

@api_view(["GET"])
@authentication_classes([TokenAuthentication])
def queryCountToday(request, user_id):
    if request.method == "GET":
        count =QuestionCountHistory.objects.filter(user=user_id,date=date.today()).values('count')
        return Response(count[0] if count.exists() else {"count":0})

@api_view(["POST"])
@authentication_classes([TokenAuthentication])
def weeklyQueryCount(request,user_id):
    if request.method== "POST":
        startDate = request.data['startDate']
        endDate = request.data['endDate']
        data = getWeeklyQueryData(startDate,endDate,user_id)
        return Response(data)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
def switchAlgo(request):
    if request.method=="POST":
        algorithm = request.data['algorithm']
        switchAlgorithm(algorithm)
        return Response({"status":"Algorithm Switched Successfully"})

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
def index(request):
    return render(request, "bertConnector/indexApi.html")
