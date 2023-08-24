import json
import requests
from urllib.parse import urljoin
from types import SimpleNamespace

from aibloks.errors import AiBloksException

class Requestor():
    def __init__(self, username, api_key, endpoint_url):
        self.session = requests.Session()
        self.session.auth = (username, api_key)
        self.endpoint_url = endpoint_url

    def make_request(self, method, route, headers=None, params=None, json=None, files=None):
        url = urljoin(self.endpoint_url, route)
        with self.session.request(method=method, url=url, headers=headers, params=params, json=json, files=files) as response:
            if response.status_code > 203:   # TODO: Better, more explicit error handling
                raise AiBloksException(response)       
        return response
    
    def json_to_obj(self, json_dict):
        return json.loads(json_dict, object_hook=lambda d: SimpleNamespace(**d))