from django.contrib.auth.views import LogoutView

from django.urls import path

from .views import *

app_name = 'b2d'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('businesses/', BusinessListView.as_view(), name='search_page'),
    path('business/<int:pk>/', BusinessDetailView.as_view(), name='business_detail'),
    path('business-profile', BusinessProfileView.as_view(), name='business_profile'),
    path('register/', RegistrationFormView.as_view(), name='registration'),
    path('login/', B2DLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]

