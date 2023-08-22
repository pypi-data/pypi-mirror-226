import json
import time

from . import project
from .api import _api_session

from ..utils.config import CLIENT_ID
import webbrowser


def get_oauth_instance():

    apiKey = CLIENT_ID
    if not apiKey:
        apiKey = input("Enter your flockfysh client id. This can be found in the 'Settings' page of your profile: ").strip()
    
    print(str(apiKey))
    
    new_instance = _api_session.post("/api/users/auth/register", data={
        "scope": "write_dataset read_dataset share_dataset manage_account",
        "apiKey": str(apiKey),
    }).json()['data']
    
    return new_instance["data"]


def poll_oauth_instance(deviceCode):
    while True:
        time.sleep(2)
        private_instance = _api_session.post("/api/users/auth/getAccessToken/private", data={
            "deviceCode": deviceCode
        }).json()["data"]["data"]


        state = private_instance['state']
        if state == "approved":
            return private_instance["access_token"]["access_token"]
        elif state == "rejected":
            raise Exception("Login cancelled.")
        elif state == "expired":
            raise Exception("Login session expired. Try logging in again.")


@project._check_flockfysh_dir
def login(open_window=True):
    new_instance = get_oauth_instance()

    print(new_instance)
    if open_window:
        webbrowser.open(new_instance["url"])
    else:
        print(f"Go to {new_instance['url']} to log in to the CLI.")

    print(new_instance['device_code'])
    access_token = poll_oauth_instance(new_instance["device_code"])
    with open(project.flockfysh_path("credentials.json"), "w") as file:
        json.dump({
            "access_token": access_token
        }, file)
