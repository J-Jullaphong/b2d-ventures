from django.contrib import admin
from django.contrib.auth.models import Group, User

from .investor_registration_admin import InvestorRegistrationAdmin
from .business_registration_admin import BusinessRegistrationAdmin
from .fundraising_admin import FundraisingAdmin

admin.site.index_title = ''
admin.site.unregister(Group)
admin.site.unregister(User)
