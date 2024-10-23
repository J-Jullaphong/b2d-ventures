import logging

from django.contrib.auth.views import LoginView
from django.contrib import messages
from django_otp.forms import OTPAuthenticationForm

db_logger = logging.getLogger('db')


class B2DLoginView(LoginView):
    template_name = 'b2d/login.html'
    next_page = "b2d:home"
    authentication_form = OTPAuthenticationForm

    def form_valid(self, form):
        """User successful login"""
        user = form.get_user()
        db_logger.info(f"User {user.id} successful login")
        messages.success(self.request, f"Login successful. Welcome {user.username}.")
        return super().form_valid(form)
