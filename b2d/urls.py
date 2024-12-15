from django.contrib.auth.views import LogoutView

from django.urls import path

from .views import *

app_name = 'b2d'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('profile/', InvestorProfileView.as_view(), name='investor_profile'),
    path('businesses/', BusinessListView.as_view(), name='search_page'),
    path('business/<uuid:pk>/', BusinessDetailView.as_view(), name='business_detail'),
    path('business-profile/', BusinessProfileView.as_view(), name='business_profile'),
    path('fundraise/', FundRaisingDashboardView.as_view(), name='fundraising'),
    path('fundraise/<uuid:fundraise_id>/invest/', InvestmentView.as_view(), name='invest_fundraise'),
    path('portfolio/', PortfolioView.as_view(), name='portfolio'),
    path('register/', RegistrationFormView.as_view(), name='registration'),
    path('login/', B2DLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('learn-more/', LearnMoreView.as_view(), name='learn_more'),
    path('privacy-notice/', PrivacyPolicyView.as_view(), name='privacy_notice'),
]

