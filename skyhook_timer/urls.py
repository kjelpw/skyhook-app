from django.urls import path
from . import views

app_name = 'skyhook_timer'

urlpatterns = [
    path('timers/', views.skyhook_timer_view, name='view_timers'),
]
