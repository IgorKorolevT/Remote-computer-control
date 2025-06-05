import asyncio
from typing import Union, List, Tuple
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from bs4.element import PageElement, Tag, NavigableString
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from command.models import Command, Parameter
import aiohttp

DEFAULT_OS = "Windows"
_Content = Union[PageElement, Tag, NavigableString]
Examples = List[str]
Parameters = List[Tuple[str, str]]
User = get_user_model()


def _get_command_url(detail_command_url: str, command_url_prefix: str) -> str:
    """Return full detail url for this command"""
    return urljoin(detail_command_url, command_url_prefix)


async def _get_soup_async(session: aiohttp.ClientSession, url: str, features="html.parser"):
    async with session.get(url) as response:
        response.raise_for_status()
        text = await response.text()
        soup = BeautifulSoup(text, features)
        return soup


async def create_command(update: bool, author: User, name: str, command: str, description: str, syntax: str,
                         examples: Examples,
                         parameters: Parameters, os: str, source: str = None) -> Command:
    """Add or update command"""
    try:
        if update:
            command = await Command.objects.aupdate_or_create(author=author, name=name, command=command,
                                                              description=description, syntax=syntax,
                                                              examples=examples, os=os, source=source)
            command = command[0]
            for parameter in parameters:
                await Parameter.objects.aupdate_or_create(parameter_name=parameter[0], description=parameter[1],
                                                          command=command)
        else:
            command = await Command.objects.acreate(author=author, name=name, command=command,
                                                    description=description, syntax=syntax,
                                                    examples=examples, os=os, source=source)
            for parameter in parameters:
                await Parameter.objects.acreate(parameter_name=parameter[0], description=parameter[1],
                                                command=command)
    except IntegrityError as e:
        print(f"Command {name} has already created")
    return command


async def async_parse_command(url: str, update: bool = False, session: aiohttp.ClientSession = None,
                              author: User = None,
                              os: str = DEFAULT_OS) -> None:
    """Parse one command and save it to db"""
    if session is None:
        session = aiohttp.ClientSession()

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
    else:
        await create_command(author=author, name=name, command=name, description=description, syntax=syntax,
                             examples=examples, update=update,
                             parameters=parameters, source=url, os=os)
    return None


async def _get_author(author_username: str) -> User:
    author = await get_user_model().objects.aget(username=author_username)
    return author


async def async_parse_commands(home_url: str, detail_command_url: str, author_username: str, update: bool = False,
                               os: str = DEFAULT_OS) -> None:
    """Async parse all commands from the main commands page."""
    author = await _get_author(author_username)

    async with aiohttp.ClientSession() as session:
        try:
            soup = await _get_soup_async(session, home_url)

            commands = soup.find_all("a", {"data-linktype": "relative-path"})
            # Delete duplication cscript and wscript
            commands = commands[2:]
            tasks = list()
            for command in commands:
                command_url = _get_command_url(detail_command_url, command.get("href"))
                tasks.append(asyncio.create_task(
                    async_parse_command(update=update, url=command_url, author=author, os=os, session=session)))
            print(f"The total number of commands is {len(tasks)}")
            await asyncio.gather(*tasks)
        except aiohttp.ClientError as e:
            print(f"Error fetching main page: {str(e)}")
        except asyncio.TimeoutError as e:
            print("Time out")


def parse_commands(home_url: str, detail_command_url: str, author_username: str, update: bool = False,
                   os: str = DEFAULT_OS) -> None:
    """Parse all commands from the main commands page."""
    try:
        asyncio.run(async_parse_commands(update=update, author_username=author_username, os=os, home_url=home_url,
                                         detail_command_url=detail_command_url))
    except KeyboardInterrupt as e:
        print("Cancelled parser")
