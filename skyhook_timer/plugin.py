from allianceauth.plugins import app_module
from django.utils.translation import gettext_lazy as _

class SkyhookTimerPlugin(app_module.AppPlugin):
    name = "Skyhook Timer Plugin"
    author = "Your Name"
    version = "0.0.2"
    description = _("Skyhook Timer Plugin for managing timers.")
    url_slug = "skyhook_timer"
    menu_include = True  # This ensures the plugin shows in the admin menu
    menu_name = _("Skyhook Timers")  # Name to display in the menu

    def ready(self):
        super().ready()
        # Register the model in the admin interface
        import skyhook_timer.admin  # Import admin.py to register models
