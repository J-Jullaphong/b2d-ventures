import logging

from django.contrib import messages
from django.contrib.auth.models import User
from django.views.generic import TemplateView

from ..forms import InvestorRegistrationForm, BusinessRegistrationForm

db_logger = logging.getLogger('db')


class RegistrationFormView(TemplateView):
    """View for handling the registration process for both investors and businesses."""
    template_name = 'b2d/registration.html'

    def get_context_data(self, **kwargs):
        """Adds the appropriate registration form to the context based on the query parameter."""
        context = super().get_context_data(**kwargs)

        if 'form' not in context:
            form_type = self.request.GET.get('form', 'investor')
            if form_type == 'business':
                context['form'] = BusinessRegistrationForm()
            else:
                context['form'] = InvestorRegistrationForm()

        return context

    def post(self, request, *args, **kwargs):
        """Handles POST requests for form submissions."""
        form_type = self.request.GET.get('form', 'investor')

        if form_type == 'business':
            form = BusinessRegistrationForm(request.POST, request.FILES)
        else:
            form = InvestorRegistrationForm(request.POST, request.FILES)

        if form.is_valid():
            user = form.save()
            db_logger.info(f'User {user.id} successful registration.')
            messages.success(self.request, "Registration successful. Your account will be activated once approved.")
            return self.render_to_response(self.get_context_data(form=form))

        messages.error(self.request, "There was an error with your submission.")
        return self.render_to_response(self.get_context_data(form=form))
