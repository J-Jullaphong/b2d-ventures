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

    def form_invalid(self, form):
        """Handle unsuccessful login attempts"""
        error_messages = form.errors.as_json()
        email = self.request.POST.get('username', '....@xxx.com')
        db_logger.warning(f"Unsuccessful login attempt: {error_messages}")
        messages.error(self.request, "Login failed. Please check your credentials and try again.")
        context = self.get_context_data(form=form)
        context['user_email'] = email
        return self.render_to_response(context)
