from django.contrib import admin
from .models import SkyhookTimer

@admin.register(SkyhookTimer)
class SkyhookTimerAdmin(admin.ModelAdmin):
    list_display = ('eve_system', 'planet_number', 'countdown_time', 'time_remaining')
    search_fields = ('eve_system',)
    list_filter = ('countdown_time',)
