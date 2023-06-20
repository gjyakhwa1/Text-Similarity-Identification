from django.shortcuts import render

from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token

from accounts.helper import getWeeklyQueryData
from accounts.helper import getHighestQueryUsers
from .helper import cleanText, similaritySearch, getTimeStamp, uploadCSVFile, getCosineSimilarity
from .models import Question, QuestionCountHistory, ServerStatus
from .serializers import QuestionSerializer, ServerStatusSerializer

from datetime import date
import csv,io,threading
# Create your views here.


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
def viewQuestion(request):
    questions = Question.objects.all()
    serializeQuestion = QuestionSerializer(questions, many=True)
    return Response(serializeQuestion.data)


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
def getServerStatus(request):
    modelLoadingStatusMap = {
        0:"MODEL_LOAD",
        1:"FAISS_LOAD",
        2:"COMPLETE"
    }
    questionUpdatingStatusMap = {
        0 : "DATABASE_UPDATE",
        1:"ENCODE",
        2:"DUMP",
        3:"COMPLETE"
    }
    data =ServerStatus.objects.all().first()
    serializeData = ServerStatusSerializer(data)
    modelTimeStamp = getTimeStamp(serializeData.data["currentTimeStampModel"])-getTimeStamp(serializeData.data["startTimeStampModel"])
    questionsTimeStamp = getTimeStamp(serializeData.data["currentTimeStampQuestions"])-getTimeStamp(serializeData.data["startTimeStampQuestions"])
    return Response({"data":serializeData.data,"modelTimeStamp":modelTimeStamp.total_seconds(),"questionsTimeStamp":questionsTimeStamp.total_seconds(), "modelLoadingStatusMap":modelLoadingStatusMap,"questionUpdatingStatusMap":questionUpdatingStatusMap}, status=200)


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
        cosineSimilarity = getCosineSimilarity(ques,[cleanText(item['question']) for item in serializeQuestion.data])
        return Response({"similarQuestion":serializeQuestion.data,"cosineSimilarity":cosineSimilarity})


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
def uploadData(request):
    if request.method == "POST":
        csvFile = request.FILES.get('file')
        examinationType =request.data["examinationType"]
        examYear = request.data["examYear"]
        token_key = request.auth
        token = Token.objects.get(key=token_key)
        user = token.user
        if not csvFile:
            return Response({"error":"No CSV file provided"})
        #Parsing the CSV file
        decodedFile = csvFile.read().decode('utf-8')
        ioString = io.StringIO(decodedFile)
        reader = csv.reader(ioString)
        threading.Thread(target=uploadCSVFile,args=(reader,examinationType,examYear,user,)).start()
        # uploadCSVFile(reader)
        return Response({'success':"Completed"})

@api_view(["GET"])
@authentication_classes([TokenAuthentication])
def filterOptions(request):
    if request.method=="GET":
        options={
            "examinationYear":[],
            "examName":[]
        }
        options['examinationYear'] = Question.objects.order_by().values_list('examYear', flat=True).distinct()
        options['examName'] = Question.objects.order_by().values_list('examinationType', flat=True).distinct()
        return Response(options)

@api_view(["POST"])
@authentication_classes([TokenAuthentication])
def getQuestionsByExam(request):
    if request.method=="POST":
        results = Question.objects.filter(examYear = request.data['examYear'],examinationType=request.data['examinationType'])
        serializedData = QuestionSerializer(results, many= True)
        return Response({"results":serializedData.data})

@api_view(["GET"])
@authentication_classes([TokenAuthentication])
def getQuestionsByUser(request):
    if request.method == "GET":
        token_key = request.auth
        token = Token.objects.get(key=token_key)
        result = Question.objects.filter(user=token.user)
        serializedData = QuestionSerializer(result, many= True)
        return Response({"results":serializedData.data})

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
