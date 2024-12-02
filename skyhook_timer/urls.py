from django.urls import path
from . import views

urlpatterns = [
    path("timers/", views.timer_list, name="timer_list"),
]
