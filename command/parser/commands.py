from typing import Union, List, Tuple
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from bs4.element import PageElement, Tag, NavigableString

from command.models import Command, Parameter
from user.models import User

BASE_URL = "https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/windows-commands"
COMMAND_URL = "https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/"
type _Content = Union[PageElement, Tag, NavigableString]
type Examples = List[str]
type Parameters = List[Tuple[str, str]]


def _get_command_url(command_url_prefix: str) -> str:
    """Return full detail url for this command"""
    return urljoin(COMMAND_URL, command_url_prefix)


def _get_soup(url, features="html.parser"):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, features)
    return soup


def create_command(name: str, description: str, syntax: str, examples: Examples, parameters: Parameters) -> Command:
    """Add command to db"""
    author = User.objects.get(username="superadmin")
    command = Command.objects.create(author=author,name=name, description=description, syntax=syntax, examples=examples)
    command.save()
    for parameter in parameters:
        Parameter.objects.create(parameter_name=parameter[0], description=parameter[1], command=command).save()
    return command


def parse_command(url) -> None:
    """from url parse one command"""

    def find_syntax(content: _Content) -> str:
        h_elem = content.find("h2", {"id": "syntax"})
        syntax_text = h_elem.find_next("pre").text.strip()
        return syntax_text

    def find_examples(content: _Content) -> Examples:
        h_elem = content.find("h2", attrs={"id": "examples"})
        example_pres = h_elem.find_all_next("pre")
        examples = list(map(lambda x: x.text.strip(), example_pres))
        return examples

    def find_parameters(content: _Content) -> List[Tuple[str, str]]:
        h_elem = content.find("h3", attrs={"id": "parameters"})
        table = h_elem.find_next("table")
        columns = table.find_all("tr")[1:]
        parameters = list()
        for column in columns:
            tds = column.find_all("td")
            parm, descr = tds[0].text.strip(), tds[1].text.strip()
            parameters.append((parm, descr))
        return parameters

    soup = _get_soup(url)
    contents = soup.find_all("div", {"class": "content"})
    name = contents[0].find("h1").text
    content = contents[1]
    description = content.findChild().text
    try:
        syntax = find_syntax(content)
        examples = find_examples(content)
        parameters = find_parameters(content)
    except AttributeError as e:
        return None
    return create_command(name=name, description=description, syntax=syntax, examples=examples, parameters=parameters)


def parse_commands():
    """Parse all commands from the main commands page."""
    try:
        soup = _get_soup(BASE_URL)

        commands = soup.find_all("a", {"data-linktype": "relative-path"})
        # Delete duplication cscript and wscript
        commands = commands[2:]
        print(f"The total number of teams is {len(commands)}")
        for command in commands:
            parse_command(_get_command_url(command.get("href")))
    except requests.RequestException as e:
        print(f"Error fetching main page: {str(e)}")
    except KeyboardInterrupt as e:
        print("KeyboardInterrupt")
