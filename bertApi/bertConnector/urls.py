from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name="index"),
    path('api/questions/', views.viewQuestion, name="view-question"),
    path('api/queryQuestion/', views.queryQuestion, name="query-question"),
    path('api/serverStatus/', views.getServerStatus, name="server-status"),
    path('api/highestQueryUsers',views.highestQueryCountUsers,name='highest-query-users'),
    path('api/queryCount/<int:user_id>',views.perDayQueryCount,name='perday-query-count'),
    path('api/queryCountToday/<int:user_id>',views.queryCountToday,name='query-count-today'),
    path('api/weeklyQueryCount/<int:user_id>',views.weeklyQueryCount,name='weekly-query-count'),
    path('api/switchAlgorithm',views.switchAlgo,name="switch-algorithm"),
    path('api/uploadData',views.uploadData,name="upload-data"),
    # path('api/uploadDocument/',views.uploadDocument,name="upload-document")
]
