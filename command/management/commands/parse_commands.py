# https://docs.djangoproject.com/en/5.2/howto/custom-management-commands/
import asyncio
from django.core.management.base import BaseCommand
from command.parser.commands import parse_commands


class Command(BaseCommand):
    help = "Parse commands from microsoft"

    def add_arguments(self, parser):
        parser.add_argument(
            "--update",
            action="store_true",
            help="Update already exist commands",
        )
        parser.add_argument(
            "--author_username",
            type=str,
            default="superadmin",
            help="Author username for all commands",
        )
        parser.add_argument(
            "--home_url",
            type=str,
            default=r"https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/windows-commands",
            help="The URL where the parser will look for all commands",
        )
        parser.add_argument(
            "--command_url",
            type=str,
            default=r"https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/",
            help="The URL where the parser will look for a specific command",
        )
        parser.add_argument(
            "--os",
            type=str,
            default="windows",
            help="operating system for all commands",
        )

    def handle(self, *args, **options):
        author_username = options["author_username"]
        os = options["os"]
        home_url = options["home_url"]
        command_url = options["command_url"]
        update = options["update"]
        parse_commands(update=update, home_url=home_url, detail_command_url=command_url,
                       author_username=author_username, os=os)
