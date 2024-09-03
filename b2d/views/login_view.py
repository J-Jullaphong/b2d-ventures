from django.contrib.auth.views import LoginView


class B2DLoginView(LoginView):
    template_name = 'b2d/login.html'
    next_page = "b2d:home"
