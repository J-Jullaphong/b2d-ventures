from django.views.generic import TemplateView
from django.contrib import messages
from ..forms import InvestorRegistrationForm, BusinessRegistrationForm


class RegistrationFormView(TemplateView):
    template_name = 'b2d/registration.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        form_type = self.request.GET.get('form', 'investor')

        if form_type == 'business':
            context['form'] = BusinessRegistrationForm()
        else:
            context['form'] = InvestorRegistrationForm()

        return context

    def post(self, request, *args, **kwargs):
        form_type = self.request.GET.get('form', 'investor')

        if form_type == 'business':
            form = BusinessRegistrationForm(request.POST, request.FILES)
        else:
            form = InvestorRegistrationForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(
                self.request, "Registration successful. Your account will be activated once approved.")
            # Re-render the same page
            return self.render_to_response(self.get_context_data(form=form))

        return self.render_to_response(self.get_context_data(form=form))
