# https://docs.djangoproject.com/en/5.2/howto/custom-management-commands/
import asyncio
from django.core.management.base import BaseCommand
from command.parser.commands import async_parse_commands


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
        try:
            asyncio.run(async_parse_commands())
        except KeyboardInterrupt:
            print("Parse closed")
