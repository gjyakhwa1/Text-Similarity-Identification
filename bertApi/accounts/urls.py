from django.urls import path
from rest_framework.authtoken import views as rViews
from . import views

urlpatterns = [
    path('api-token-auth', rViews.obtain_auth_token),
    path('register',views.register,name="register-view")
    # path('api-token-auth', views.index),
    
]
