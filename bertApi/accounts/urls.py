from rest_framework.authtoken import views as rViews
from django.urls import path
from . import views

urlpatterns = [
    path('api-token-auth', rViews.obtain_auth_token),
    path('register',views.register,name="register-view"),
    path('viewUsers',views.displayAllUser,name="all-user"),
    path('profile/<int:user_id>',views.userProfile,name='user-profile'),
    path('notApproved',views.displayNotApprovedUser,name="not-approved-user"),
    path('approveUser',views.approveUser,name="approve-user"),
    path('rejectUser',views.rejectUser,name="reject-user"),
    path('login',views.loginUser,name="loginUser"),
    path('logout',views.logoutUser,name='logoutUser'),
    path('userHistory',views.userHistoryAll,name="user-history-all"),
    path('userHistory/<int:user_id>',views.userHistory,name='user-history'),
    path('getOpenAIToken',views.getOpenAIToken,name="get-openAIToken"),
    path('addOpenAIToken',views.addOpenAIToken,name="add-openAIToken")
]
