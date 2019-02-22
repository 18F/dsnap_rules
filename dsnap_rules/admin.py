from django.contrib import admin

from .models import (
    ApplicationPeriod,
    Disaster,
)

admin.site.register(ApplicationPeriod)
admin.site.register(Disaster)
