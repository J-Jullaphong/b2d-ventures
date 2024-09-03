from django.contrib import admin
from ..models import Business


@admin.register(Business)
class BusinessRegistrationAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_active')
    actions = ['approve_registration']
    fieldsets = (
        (None, {'fields': ('username', 'email', 'phone_number', 'is_active')}),
    )

    def approve_registration(self, request, queryset):
        for registration in queryset:
            if not registration.is_active:

                registration.is_active = True
                registration.save()

                self.message_user(request, f"{registration.email} approved successfully.")

    approve_registration.short_description = "Approve selected registrations"