from django.contrib import admin

from ..models import UserConsent


@admin.register(UserConsent)
class UserConsentAdmin(admin.ModelAdmin):
    """
        Admin configuration for the UserConsent model to manage user consent
        records for GDPR/PDPA compliance in the Django admin interface.
    """
    readonly_fields = ['user', 'consent_date', 'last_updated']
    list_display = ('user', 'consent', 'consent_date', 'last_updated')
    list_filter = ('consent', 'consent_date', 'last_updated')
    search_fields = ('user__username',)
    date_hierarchy = 'consent_date'
    ordering = ('-last_updated',)

    def has_add_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['title'] = 'User Consents'
        return super().changelist_view(request, extra_context=extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['title'] = f"User Consent: {object_id}"
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
