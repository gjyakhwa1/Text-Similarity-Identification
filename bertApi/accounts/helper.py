from django.utils import timezone
from django.contrib.auth import get_user_model
from django.db.models.functions import TruncWeek
from django.db.models import Sum

from .models import LoginHistory
from bertConnector.models import QuestionCountHistory

from datetime import date, timedelta

def getLogoutTime(user):
    loginHistory=LoginHistory.objects.filter(user= user).last()
    lastQuestionQuery = QuestionCountHistory.objects.filter(user=user).last()
    if lastQuestionQuery is not None:
        if lastQuestionQuery.updated_at > loginHistory.login_at:
            return lastQuestionQuery.updated_at
    return timezone.now()

def getHighestQueryUsers():
    User= get_user_model()
    queryCount = User.objects.values_list('username','totalQueryQuestion').order_by('-totalQueryQuestion')
    return dict(queryCount)

def getWeeklyQueryData(start_date,end_date,user_id):
    weeklyData = (
    QuestionCountHistory.objects.filter(date__range=(start_date, end_date),user=user_id)  # Filter the data for the date range
    .annotate(week=TruncWeek('date'))  # Truncate the date to week
    .values('week')  # Group by week
    .annotate(total=Sum('count'))  # Sum the values for each week
    )
    data=[]
    # Now you can loop through the weekly_data to get the week and total for each week:
    for weekData in weeklyData:
        weekStart = weekData['week']
        weekEnd = weekStart + timedelta(days=6)
        total = weekData['total']
        data.append({'startDate':weekStart.isoformat(),"endDate":weekEnd.isoformat(),"count":total})
    return data


