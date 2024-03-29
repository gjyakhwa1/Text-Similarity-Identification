from rest_framework import status
from rest_framework.decorators import api_view,authentication_classes
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response

from django.utils import timezone
from django.contrib.auth import get_user_model, authenticate

from .serializers import RegisterSerializer,CustomUserSerializer,LoginHistorySerializer
from .models import LoginHistory
from .helper import getLogoutTime

@api_view(['POST'])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        if request.user.is_staff and request.data['is_approved']:
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"message":"Signup request sent for admin approval."}, status=status.HTTP_200_OK)
    return Response({"error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def displayAllUser(request):
    users=get_user_model().objects.all()
    data = CustomUserSerializer(users,many=True)
    return Response(data.data)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def userProfile(request,user_id):
    if request.method == "GET":
        User=get_user_model()
        queryUser = User.objects.filter(id=user_id)
        serializer = CustomUserSerializer(queryUser,many=True)
        return Response({'queryUser':serializer.data})

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def displayNotApprovedUser(request):
    User=get_user_model()
    users=User.objects.filter(approvalStatus="Pending")
    users=CustomUserSerializer(users,many=True)
    return Response(users.data)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
def approveUser(request):
    if request.method=="POST":
        User=get_user_model()
        user=User.objects.get(id=request.data['id'])
        user.approvalStatus="Approved"
        user.save()
        return Response({'message':'User approved'})

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
def rejectUser(request):
    if request.method=="POST":
        User=get_user_model()
        user=User.objects.get(id=request.data['id'])
        user.approvalStatus="Rejected"
        user.save()
        return Response({'message':'User Rejected'})

@api_view(['POST'])
def loginUser(request):
    if request.method=="POST":
        user=authenticate(username=request.data['username'],password=request.data['password'])
        if user is not None:
            # login(request,user)
            token,_ = Token.objects.get_or_create(user=user)
            userSerializer=CustomUserSerializer(user)
            loginHistory=LoginHistory.objects.filter(user= user).last()
            if loginHistory and loginHistory.logout_at is None:
                loginHistory.logout_at=getLogoutTime(user)
                loginHistory.save()
            LoginHistory.objects.create(user=user)
            return Response({"loginStatus":"Login","token":token.key,"user":userSerializer.data})
    return Response({"loginStatus":"Can not login"})

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
def logoutUser(request):
    if request.method=="POST":
        # logout(request._request)
        token_key = request.auth
        token = Token.objects.get(key=token_key)
        user = token.user
        loginHistory=LoginHistory.objects.filter(user= user).last()
        loginHistory.logout_at=timezone.now()
        loginHistory.save()
        return Response({"loginStatus":"User has logout"})

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def userHistoryAll(request):
    if request.method=="GET":
        history=LoginHistory.objects.all()
        serializer=LoginHistorySerializer(history,many=True)
        return Response({'loginHistory':serializer.data})

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def userHistory(request,user_id):
    if request.method == "GET":
        history = LoginHistory.objects.filter(user=user_id)
        serializer = LoginHistorySerializer(history,many=True)
        return Response({'loginHistory':serializer.data})
    
@api_view(["GET"])
@authentication_classes([TokenAuthentication])
def getOpenAIToken(request):
    if request.method=="GET":
        token_key = request.auth
        token = Token.objects.get(key=token_key)
        return Response({"openAIToken":token.user.openAIToken})

@api_view(["POST"])
@authentication_classes([TokenAuthentication])
def addOpenAIToken(request):
    if request.method=="POST":
        token_key = request.auth
        token = Token.objects.get(key=token_key)
        User = get_user_model()
        user = User.objects.get(id=token.user.id)
        user.openAIToken = request.data["openAIToken"]
        user.save()
        return Response({"message":"OpenAI Token added successfully"})