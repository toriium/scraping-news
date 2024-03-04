import requests

from src.settings import SPLASH_URL


def splash_request(url: str) -> requests.Response:
    response = requests.get(url=SPLASH_URL, params={'url': url, 'wait': 2})
    return response
