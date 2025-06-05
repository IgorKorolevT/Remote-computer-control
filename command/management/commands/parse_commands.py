# https://docs.djangoproject.com/en/5.2/howto/custom-management-commands/
from django.core.management.base import BaseCommand
from command.parser.commands import parse_commands


class Command(BaseCommand):
    help = "Parse commands from microsoft"
    # def add_arguments(self, parser):
    #     parser.add_argument(
    #         "--total_number",
    #         type=int,
    #         default=10,
    #         help="Total number of courses to create",
    #     )
    #     parser.add_argument(
    #         "--root_number",
    #         type=int,
    #         default=2,
    #         help="Number of root courses to create",
    #

    def handle(self, *args, **options):
        parse_commands()
