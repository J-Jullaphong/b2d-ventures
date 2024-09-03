from django.urls import path
from django.contrib.auth.views import LogoutView, PasswordResetView
from .views import *

app_name = 'b2d'

urlpatterns = [
    path('', home, name='home'),
    path('register/', RegistrationFormView.as_view(), name='registration'),
    path('login/', B2DLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('reset-password/', PasswordResetView.as_view(), name='reset-password')
]
