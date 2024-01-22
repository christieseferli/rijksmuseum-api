import pytest
import requests


class APISession(requests.Session):
    def __init__(self, prefix_url=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prefix_url = prefix_url

    def request(self, method, url, *args, **kwargs):
        url = self.prefix_url + url
        return super().request(method, url, *args, **kwargs)


@pytest.fixture(scope='session')
def session():
    def _session(culture):
        prefix_url = f'https://www.rijksmuseum.nl/api/'
        if culture:
            prefix_url += f'{culture}/'
        session = APISession(prefix_url)
        session.headers.update({'content-type': 'application/json'})
        session.headers.update({'accept': 'application/json'})
        return session
    yield _session
