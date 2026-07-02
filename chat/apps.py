from django.apps import AppConfig
import logging
from django.db.backends.signals import connection_created

def null_channel_name(sender, connection, **kwargs):
    # This filed is need ^
    from computer.models import Computer

    logger = logging.getLogger(__name__)

    try:
        Computer.objects.update(channel_name=None)
        logger.debug(f"Set channel_name to none")
    except Exception as e:
        logger.error(f"Can't set none channel_name in computers due to:{e}")

class ChatConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "chat"

    def ready(self):
        connection_created.connect(null_channel_name)
