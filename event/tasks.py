from typing import List

from celery import shared_task
from asgiref.sync import async_to_sync

from chat.utils import send_message_to_computer
from event.models import Program
import logging

logger = logging.getLogger(__name__)

@shared_task
def kill_programs_task(user_id: int, computer_name: str):
    """Don't create/save message to db"""
    task_list = "tasklist"
    result = async_to_sync(send_message_to_computer)(user_id, computer_name, task_list, False)
    logger.error(result)
