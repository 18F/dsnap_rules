from django.contrib import admin

from .forms import ApplicationPeriodForm, DisasterForm
from .models import ApplicationPeriod, Disaster


class ApplicationPeriodInline(admin.TabularInline):
    form = ApplicationPeriodForm
    model = ApplicationPeriod
    extra = 1


class DisasterAdmin(admin.ModelAdmin):
    form = DisasterForm
    inlines = [ApplicationPeriodInline]
    list_display = ('disaster_request_no', 'title', 'state',
                    'benefit_begin_date', 'benefit_end_date')
    fields = (
        ('disaster_request_no', 'title'),
        'state',
        ('benefit_begin_date', 'benefit_end_date'),
        ('residency_required', 'uses_DSED', 'allows_food_loss_alone'),
    )
    search_fields = ['state__name', 'title']


admin.site.register(Disaster, DisasterAdmin)
