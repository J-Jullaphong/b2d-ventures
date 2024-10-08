from django.contrib import admin

from ..models import Business


@admin.register(Business)
class BusinessRegistrationAdmin(admin.ModelAdmin):
    """
        Customizes the admin interface for the Business model, allowing for
        business registration approvals and management.
    """
    list_display = ('name', 'email', 'business_registration_certificate',
                    'tax_identification_number',
                    'proof_of_address', 'financial_statements',
                    'ownership_documents',
                    'director_identification', 'licenses_and_permits',
                    'bank_account_details', 'is_active')
    actions = ['approve_registration']
    fieldsets = (
        (None, {'fields': (
            'name', 'email', 'phone_number',
            'business_registration_certificate',
            'tax_identification_number',
            'proof_of_address', 'financial_statements',
            'ownership_documents',
            'director_identification', 'licenses_and_permits',
            'bank_account_details', 'is_active')}),
    )

    def approve_registration(self, request, queryset):
        """Custom action to approve selected business registrations."""
        for registration in queryset:
            if not registration.is_active:
                registration.is_active = True
                registration.save()

                self.message_user(request,
                                  f"{registration.email} approved successfully.")

    approve_registration.short_description = "Approve selected registrations"
