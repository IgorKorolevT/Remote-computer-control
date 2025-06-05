import asyncio
from typing import Union, List, Tuple
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from bs4.element import PageElement, Tag, NavigableString
from django.db import IntegrityError

from command.models import Command, Parameter
from user.models import User
import aiohttp

BASE_URL = "https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/windows-commands"
COMMAND_URL = "https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/"
AUTHOR = User.objects.get(username="superadmin")
type _Content = Union[PageElement, Tag, NavigableString]
type Examples = List[str]
type Parameters = List[Tuple[str, str]]


def _get_command_url(command_url_prefix: str) -> str:
    """Return full detail url for this command"""
    return urljoin(COMMAND_URL, command_url_prefix)


async def _get_soup_async(session: aiohttp.ClientSession, url: str, features="html.parser"):
    async with session.get(url) as response:
        response.raise_for_status()
        text = await response.text()
        soup = BeautifulSoup(text, features)
        return soup


async def create_command(name: str, command: str, description: str, syntax: str, examples: Examples,
                         parameters: Parameters, os: str = "Windows", source: str = None) -> Command:
    """Add or update command"""
    try:
        command = await Command.objects.aupdate_or_create(author=AUTHOR, name=name, command=command,
                                                          description=description, syntax=syntax,
                                                          examples=examples, os=os, source=source)
        command = command[0]
        for parameter in parameters:
            await Parameter.objects.aupdate_or_create(parameter_name=parameter[0], description=parameter[1],
                                                      command=command)
    except IntegrityError as e:
        pass
        # print(f"Command {name} already exists")
    return command


async def async_parse_command(session: aiohttp.ClientSession, url: str) -> None:
    """from url parse one command"""

    def find_syntax(content: _Content) -> str:
        h_elem = content.find("h2", {"id": "syntax"})
        syntax_text = h_elem.find_next("pre").text.strip()
        return syntax_text

    def find_examples(content: _Content) -> Examples:
        h_elem = content.find("h2", attrs={"id": "examples"})
        examples = list()
        if h_elem:
            example_pres = h_elem.find_all_next("pre")
            examples = list(map(lambda x: x.text.strip(), example_pres))
        return examples

    def find_parameters(content: _Content) -> List[Tuple[str, str]]:
        h_elem = content.find("h3", attrs={"id": "parameters"})
        parameters = list()
        if h_elem:
            table = h_elem.find_next("table")
            columns = table.find_all("tr")[1:]
            for column in columns:
                tds = column.find_all("td")
                parm, descr = tds[0].text.strip(), tds[1].text.strip()
                parameters.append((parm, descr))
        return parameters

    soup = await _get_soup_async(session, url)
    contents = soup.find_all("div", {"class": "content"})
    name = contents[0].find("h1").text
    content = contents[1]
    description = content.findChild().text
    try:
        syntax = find_syntax(content)
        examples = find_examples(content)
        parameters = find_parameters(content)
    except AttributeError as e:
        print(f"Command {name} has no created")
        return None

    await create_command(name=name, command=name, description=description, syntax=syntax, examples=examples,
                         parameters=parameters, source=url)
    return None


async def async_parse_commands():
    """Parse all commands from the main commands page."""
    async with aiohttp.ClientSession() as session:
        try:
            soup = await _get_soup_async(session, BASE_URL)

            commands = soup.find_all("a", {"data-linktype": "relative-path"})
            # Delete duplication cscript and wscript
            commands = commands[2:]
            tasks = list()
            for command in commands:
                command_url = _get_command_url(command.get("href"))
                tasks.append(asyncio.create_task(async_parse_command(session, command_url)))
            print(f"The total number of teams is {len(tasks)}")
            await asyncio.gather(*tasks)
        except aiohttp.ClientError as e:
            print(f"Error fetching main page: {str(e)}")
        except asyncio.TimeoutError as e:
            print("KeyboardInterrupt")
