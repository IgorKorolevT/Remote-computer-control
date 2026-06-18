from celery import shared_task
from asgiref.sync import async_to_sync

from chat.utils import send_message_to_computer
import logging

from event.utils import get_programs

logger = logging.getLogger(__name__)

@shared_task
def kill_programs_task(user_id: int, computer_name: str):
    """Don't create/save message to db"""
    programs = get_programs(user_id, computer_name)
    # TODO replace to another file
    process_names = []
    for program in programs:
        name = program.name.strip()
        if not name:
            continue
        if '.' in name:
            process_names.append(name)
        else:
            # If there is no extension, try both options
            process_names.append(name)
            process_names.append(name + ".exe")
    processes_str = " /im ".join(process_names)
    cmd = f'taskkill /f /fi "username eq %username%" /im {processes_str}'
    logger.debug(cmd)

    result = async_to_sync(send_message_to_computer)(user_id, computer_name, cmd, False)

    return result