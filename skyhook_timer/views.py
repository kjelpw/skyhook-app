from django.shortcuts import render
from .models import SkyhookTimer

def timer_list(request):
    timers = SkyhookTimer.objects.all()
    return render(request, "skyhook_timer/timer_list.html", {"timers": timers})
