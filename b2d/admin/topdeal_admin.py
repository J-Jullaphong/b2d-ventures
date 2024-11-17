from django.contrib import admin
from django.utils import timezone

from ..models import TopDeal, FundRaising


@admin.register(TopDeal)
class TopDealAdmin(admin.ModelAdmin):
    list_display = ('fundraising', 'display_order')
    ordering = ('display_order',)
    search_fields = ('fundraising__business__name',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """
        Customize the queryset for the fundraising field to show sorted fundraisers.
        """
        if db_field.name == "fundraising":
            kwargs["queryset"] = FundRaising.objects.filter(
                fundraising_status='approve',
                publish_date__lte=timezone.now(),
                deadline_date__gt=timezone.now()
            ).order_by('business__name')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['title'] = 'Top Deals'
        return super().changelist_view(request, extra_context=extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['title'] = f"Top Deals"
        extra_context['subtitle'] = None
        return super().change_view(request, object_id, form_url, extra_context=extra_context)
