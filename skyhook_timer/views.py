from django.shortcuts import render
from django.http import HttpResponseForbidden
from django.contrib.auth.models import Group
from .models import SkyhookTimer

def skyhook_timer_view(request):
    if not request.user.groups.filter(name='Member').exists() and not request.user.is_superuser:
        return HttpResponseForbidden("You do not have permission to view this plugin.")

    # Get all timers for the member to view
    timers = SkyhookTimer.objects.all()

    # Render the view, allow "Members" to see but not interact with the data
    return render(request, 'skyhook_timer/view_timers.html', {'timers': timers})
