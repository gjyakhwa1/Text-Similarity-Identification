from django.contrib.auth.backends import BaseBackend
from .models import CustomUser

class MyAuthBackend(BaseBackend):
    """
    A custom authentication backend that authenticates users
    using their email address instead of their username.
    """

    def authenticate(self, request, username, password=None, **kwargs):
        try:
            user = CustomUser.objects.get(username=username)
            if user.check_password(password):
                return user
        except CustomUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None