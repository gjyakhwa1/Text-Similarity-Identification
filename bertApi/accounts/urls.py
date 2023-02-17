from django.urls import path
from rest_framework.authtoken import views as rViews
from . import views

urlpatterns = [
    path('api-token-auth', rViews.obtain_auth_token),
    path('register',views.register,name="register-view"),
    path('notapproved',views.displayNotApprovedUser,name="not-approved-user"),
    path('approveuser',views.approveUser,name="approve-user"),
    path('rejectuser',views.rejectUser,name="reject-user"),
    path('login',views.loginUser,name="loginUser"),
    path('logout',views.logoutUser,name='logoutUser'),
    path('userHistory',views.userHistoryAll,name="user-history-all"),
    path('userHistory/<int:user_id>',views.userHistory,name='user-history')
]
