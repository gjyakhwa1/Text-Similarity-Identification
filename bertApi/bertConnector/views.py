from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User, Group
from django.shortcuts import render

from rest_framework import permissions
from rest_framework.generics import ListAPIView

from .serializers import UserSerializer, GroupSerializer

from .helper import cleanText, similaritySearch
from .models import Question

# Create your views here.


class UserViewSet(ListAPIView):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(ListAPIView):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


def index(request):
    context = {}
    if request.method == 'POST':
        ques = request.POST['ques']
        ques = cleanText(ques)
        similarQuesId = similaritySearch(ques)
        similarQuesId = similarQuesId+1
        context['ques'] = Question.objects.filter(pk__in=similarQuesId)
    return render(request, 'bertConnector/ques.html', context)
