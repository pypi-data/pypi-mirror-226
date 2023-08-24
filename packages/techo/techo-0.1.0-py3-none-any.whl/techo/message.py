"""
Send a message (currently only to 2482122432)
"""

from pathlib import Path
import requests

here = Path(__file__).parent
API_KEY_FILE = here/'.techo_api_key'
API_PATH = 'https://c5wl8nyro0.execute-api.us-east-2.amazonaws.com/prod/'


def has_api_key() -> bool:
    return API_KEY_FILE.exists()


def store_api_key(key: str):
    API_KEY_FILE.write_text(key)


def get_api_key() -> str:
    return API_KEY_FILE.read_text()


def send(message: str):
    """Send msg to /send."""

    headers = {
        'x-api-key': get_api_key(),
        'Content-Type': 'application/json',
    }

    resp = requests.post(
        url=API_PATH + 'send',
        json={'message': message},
        headers=headers,
    )

    if resp.status_code != 200:
        raise Exception(f'Error sending text: {resp}')
