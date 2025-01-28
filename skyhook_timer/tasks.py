from celery import shared_task
from discord import SyncWebhook, Embed
from datetime import datetime, timedelta
from django.utils.timezone import now
from django.conf import settings

from skyhook_timer.models import SkyhookTimer

@shared_task
def notify_skyhook_timer():
    """
    Notifies about an upcoming Skyhook timer via Discord.
    """
    for timer in SkyhookTimer.objects.all():
        time_remaining = timer.time_remaining
        # Ensure the timer is still active and is 30 minutes away (exact window)
        if time_remaining and timedelta(minutes=30) >= time_remaining > timedelta(minutes=29):
            # Send the Discord notification
            send_skyhook_notification(
                timer_name=f"{timer.eve_system} - Planet {timer.planet_number}",
                eve_system=timer.eve_system,
                time_remaining=format_time_from_properties(timer),
                webhook_url=getattr(settings, "SKYHOOK_WEBHOOK_URL")
            )


def send_skyhook_notification(timer_name, eve_system, time_remaining, webhook_url):
    """
    Sends a Discord notification for an upcoming Skyhook event.

    Args:
        timer_name (str): Name of the Skyhook event.
        eve_system (str): Name of the EVE system.
        time_remaining (str): Time left until the event.
        webhook_url (str): Discord webhook URL.
    """
    # Create the webhook instance
    webhook = SyncWebhook.from_url(webhook_url)
    
    # Create an embed for the notification
    embed = Embed(
        title="Skyhook Timer Alert",
        description=f"The timer **{timer_name}** is about to expire!",
        color=0xFFFF00,  # Yellow color for warning
        timestamp=datetime.utcnow(),
    )
    embed.add_field(name="EVE System", value=eve_system, inline=False)
    embed.add_field(name="Time Remaining", value=time_remaining, inline=False)
    embed.set_footer(text="Skyhook Timer Notification")
    
    # Send the notification
    webhook.send(embed=embed, username="Skyhook Timer")


def format_time_from_properties(timer):
    """
    Formats time remaining using the properties of the SkyhookTimer model.
    
    Args:
        timer (SkyhookTimer): Timer instance to format.
    
    Returns:
        str: Formatted time remaining as a string.
    """
    if not timer.time_remaining:
        return "Time expired"

    parts = []
    if timer.time_remaining.days > 0:
        parts.append(f"{timer.time_remaining.days}d")
    if timer.hours_remaining:
        parts.append(f"{timer.hours_remaining}h")
    if timer.minutes_remaining:
        parts.append(f"{timer.minutes_remaining}m")
    if timer.seconds_remaining:
        parts.append(f"{timer.seconds_remaining}s")

    return " ".join(parts)
