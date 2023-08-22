import json
import sys
import requests
from . import project
from urllib.parse import urljoin

_API_URL = "https://api.flockfysh.ai"

class BaseUrlSession(requests.Session):
    def __init__(self, base_url=None):
        super().__init__()
        self._authorization = None
        try:
            with open(project.flockfysh_path("credentials.json"), "r") as file:
                self._authorization = json.load(file)["access_token"]
        except (IOError, TypeError, KeyError):
            pass
        self._base_url = base_url

    def request(self, method, url, *args, **kwargs):
        joined_url = urljoin(self._base_url, url)
        if self._authorization:
            headers = {
                **kwargs.get("headers", {}),
                "Authorization": f"Bearer {self._authorization}",
            }
        else:
            headers = kwargs.get("headers", {})
        return super().request(method, joined_url, *args, **kwargs, headers=headers)

    def _authorization_check(self, func):
        def checker(*args, **kwargs):
            if self._authorization is None:
                raise Exception("You need to log in to use Flockfysh CLI.")

            result = self.get("/api/users/auth/").json()
            
            
            if not result["success"] and result["error"]["code"] == "ERROR_UNAUTHORIZED":
                raise Exception("Your Flockfysh CLI credentials are not valid. Please try logging in again.")
            
            elif 'success' not in result:
                raise Exception("Authorization failed")
            
            return func(*args, **kwargs)

        return checker


_api_session = BaseUrlSession(_API_URL)
