from django.contrib.auth.views import LoginView
from django_otp.forms import OTPAuthenticationForm


class B2DLoginView(LoginView):
    template_name = 'b2d/login.html'
    next_page = "b2d:home"
    authentication_form = OTPAuthenticationForm
