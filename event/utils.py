from typing import List

from computer.models import Computer
from event.models import Program


def get_programs(user_id: int, computer_name: str) -> List[Program]:
    """Get list of programs for a given user and computer"""
    computer = Computer.objects.get(name=computer_name)
    programs = list(computer.programs.filter(user_id=user_id).distinct())

    return programs