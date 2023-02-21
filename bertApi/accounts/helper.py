from django.utils import timezone

from .models import LoginHistory
from bertConnector.models import QuestionCountHistory

def getLogoutTime(user):
    loginHistory=LoginHistory.objects.filter(user= user).last()
    lastQuestionQuery = QuestionCountHistory.objects.filter(user=user).last()
    if lastQuestionQuery is not None:
        if lastQuestionQuery.updated_at > loginHistory.login_at:
            return lastQuestionQuery.updated_at
    return timezone.now()
