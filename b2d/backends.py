from django.contrib.auth.backends import ModelBackend
from .models import Business, Investor


class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = Business.objects.get(email=username)
        except Business.DoesNotExist:
            try:
                user = Investor.objects.get(email=username)
            except Investor.DoesNotExist:
                return None
        if (user.check_password(password) and self.user_can_authenticate(user)
                and user.is_active):
            return user
        return None
