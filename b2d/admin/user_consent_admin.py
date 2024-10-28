from django.contrib import admin

from ..models import UserConsent


@admin.register(UserConsent)
class UserConsentAdmin(admin.ModelAdmin):
    """
        Admin configuration for the UserConsent model to manage user consent
        records for GDPR/PDPA compliance in the Django admin interface.
    """
    list_display = ('user', 'consent', 'consent_date', 'last_updated')
    list_filter = ('consent', 'consent_date', 'last_updated')
    search_fields = ('user__username',)
    date_hierarchy = 'consent_date'
    ordering = ('-last_updated',)

    def get_readonly_fields(self, request, obj=None):
        """Specifies fields that should be read-only in the admin interface."""
        if obj:
            return ['consent_date', 'last_updated']
        return []
