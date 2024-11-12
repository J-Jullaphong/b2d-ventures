from django.contrib import admin
from django.contrib.auth.models import Group

from .investor_registration_admin import InvestorRegistrationAdmin
from .business_registration_admin import BusinessRegistrationAdmin
from .fundraising_admin import FundraisingAdmin
from .investment_admin import InvestmentAdmin
from .user_consent_admin import UserConsentAdmin

admin.site.index_title = ''
admin.site.unregister(Group)
