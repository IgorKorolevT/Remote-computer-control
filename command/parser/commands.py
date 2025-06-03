import re
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


def parse_commands():
    """Parse all commands from the main commands page."""
    BASE_URL = "https://learn.microsoft.com/uk-ua/windows-server/administration/windows-commands/windows-commands"

    try:
        response = requests.get(BASE_URL)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        command = soup.find("nav", {"id": "taffixed-left-container"})
        print(command.text)
    except requests.RequestException as e:
        print(f"Error fetching main page: {str(e)}")
    except Exception as e:
        print(f"Error parsing commands: {str(e)}")
