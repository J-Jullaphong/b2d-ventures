from django.contrib import admin

from ..models import Investor


@admin.register(Investor)
class InvestorRegistrationAdmin(admin.ModelAdmin):
    """
        Customizes the admin interface for the Investor model, enabling the
        management and approval of investor registrations.
    """
    readonly_fields = ['first_name', 'last_name', 'email', 'phone_number',
                       'financial_statements']
    list_display = ('first_name', 'last_name', 'email', 'is_active',
                    'financial_statements')
    actions = ['approve_registration']
    fieldsets = (
        ("Information", {'fields': (
            'first_name', 'last_name', 'email', 'phone_number',
            'financial_statements', 'is_active')}),
    )
    list_filter = ('is_active',)

    def has_add_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['title'] = 'Investor Registrations'
        return super().changelist_view(request, extra_context=extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['title'] = f"Investor Registration: {object_id}"
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
        """Custom action to approve selected investor registrations."""
        for registration in queryset:
            if not registration.is_active:
                registration.is_active = True
                registration.save()

                self.message_user(request,
                                  f"{registration.email} approved successfully.")

    approve_registration.short_description = "Approve selected registrations"
