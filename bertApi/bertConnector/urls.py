from django.urls import path, include

from . import views


urlpatterns = [
    path('', views.index, name="index"),
    path('api/question/', views.viewQuestion, name="view-question"),
    path('api/test/', views.test, name="test"),
    path('api/queryQuestion/', views.queryQuestion, name="query-question"),
]
