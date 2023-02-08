from rest_framework import status
from rest_framework.decorators import api_view,authentication_classes, permission_classes
from django.contrib.auth import get_user_model, authenticate, login, logout
from .serializers import RegisterSerializer,CustomUserSerializer,LoginHistorySerializer
from rest_framework.response import Response
from .models import LoginHistory
from django.utils import timezone

@api_view(['POST'])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        if request.user.is_staff and request.data['is_approved']:
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"message":"Signup request sent for admin approval."}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def displayNotApprovedUser(request):
    User=get_user_model()
    users=User.objects.filter(is_approved=False)
    users=CustomUserSerializer(users,many=True)
    return Response(users.data)

@api_view(['POST'])
def approveUser(request):
    if request.method=="POST":
        User=get_user_model()
        user=User.objects.get(username=request.data['username'])
        user.is_approved=True
        user.save()
        return Response({'message':'User approved'})

@api_view(['POST'])
def loginUser(request):
    if request.method=="POST":
        user=authenticate(username=request.data['username'],password=request.data['password'])
        if user is not None:
            login(request,user)
            LoginHistory.objects.create(user=user)
            return Response({"LoginStatus":"Login"})
    return Response({"LoginStatus":"Can not login"})

@api_view(['POST'])
def logoutUser(request):
    if request.method=="POST":
        logout(request._request)
        loginHistory=LoginHistory.objects.filter(user= request.user).last()
        loginHistory.logout_at=timezone.now()
        loginHistory.save()
        return Response({"LoginStatus":"User has logout"})

@api_view(['GET'])
def userHistoryAll(request):
    history=LoginHistory.objects.all()
    serializer=LoginHistorySerializer(history,many=True)
    return Response({'loginHistory':serializer})
