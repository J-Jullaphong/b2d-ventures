from django.contrib import admin
from django.contrib.auth.views import (PasswordResetView,
                                       PasswordResetConfirmView,
                                       PasswordResetDoneView,
                                       PasswordResetCompleteView)
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('b2d.urls')),
    path('reset-password/',
         PasswordResetView.as_view(
             template_name='registration/password_reset.html'),
         name='password_reset'),
    path('reset-password/done/',
         PasswordResetDoneView.as_view(
             template_name='registration/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(
             template_name='registration/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('reset-password-complete/',
         PasswordResetCompleteView.as_view(
             template_name='registration/password_reset_complete.html'),
         name='password_reset_complete'),
]
