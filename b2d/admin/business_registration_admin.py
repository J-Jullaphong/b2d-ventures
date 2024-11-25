from django.contrib import admin

from ..models import Business


@admin.register(Business)
class BusinessRegistrationAdmin(admin.ModelAdmin):
    """
        Customizes the admin interface for the Business model, allowing for
        business registration approvals and management.
    """
    readonly_fields = (
        'name', 'email', 'phone_number', 'business_registration_certificate',
        'tax_identification_number',
        'proof_of_address', 'financial_statements',
        'ownership_documents',
        'director_identification', 'licenses_and_permits',
        'bank_account_details')
    list_display = ('name', 'email', 'is_active')
    actions = ['approve_registration']
    fieldsets = (
        ("Information", {'fields': (
            'name', 'email', 'phone_number', 'is_active')}),
        ("Documentations", {'fields': (
            'business_registration_certificate',
            'tax_identification_number',
            'proof_of_address', 'financial_statements',
            'ownership_documents',
            'director_identification', 'licenses_and_permits',
            'bank_account_details')}),
    )
    list_filter = ('is_active',)

    def has_add_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['title'] = 'Business Registrations'
        return super().changelist_view(request, extra_context=extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['title'] = f"Business Registration: {object_id}"
        extra_context['subtitle'] = None
        return super().change_view(request, object_id, form_url,
                                   extra_context=extra_context)

    def render_change_form(self, request, context, add=False, change=False,
                           form_url='', obj=None):
        context.update({
            'show_save_and_continue': False,
            'show_save_and_add_another': False,
            'show_delete': False
        })
        return super().render_change_form(request, context, add, change,
                                          form_url, obj)

    def approve_registration(self, request, queryset):
        """Custom action to approve selected business registrations."""
        for registration in queryset:
            if not registration.is_active:
                registration.is_active = True
                registration.save()

                self.message_user(request,
                                  f"{registration.email} approved successfully.")

    approve_registration.short_description = "Approve selected registrations"
