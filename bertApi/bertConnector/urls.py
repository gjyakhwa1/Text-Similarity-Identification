from django.urls import path, include
# from rest_framework import routers

from . import views


# router = routers.DefaultRouter()
# router.register(r'users', views.UserViewSet)
# router.register(r'groups', views.GroupViewSet)

urlpatterns = [
    path('', views.index, name="index"),
    path('user', views.UserViewSet.as_view(), name="userView"),
    path('group', views.GroupViewSet.as_view(), name="groupView")
    # path('', include(router.urls)),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
