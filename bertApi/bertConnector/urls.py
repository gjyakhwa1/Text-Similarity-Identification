from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name="index"),
    path('api/question/', views.viewQuestion, name="view-question"),
    path('api/queryQuestion/', views.queryQuestion, name="query-question"),
    path('api/test/', views.test, name="test"),
    path('api/uploadDocument/',views.uploadDocument,name="upload-document")
]
