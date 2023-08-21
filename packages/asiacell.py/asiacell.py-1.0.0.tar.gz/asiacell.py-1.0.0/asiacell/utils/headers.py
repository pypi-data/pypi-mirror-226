import sys
from ujson import dumps

from .helpers import get_api_key, generate_device_id

access_token = None
refresh_token = None
handshake_token = None
device_id = generate_device_id()


class Headers:
    def __init__(self, data=None):
        self.headers = {
            "X-ODP-API-KEY": get_api_key(),
            "DeviceID": device_id,
            "X-OS-Version": "9",
            "X-Device-Type": f"[Python][Asia][{sys.version}] [O_MR1]",
            "X-ODP-APP-VERSION": "3.5.3",
            "X-FROM-APP": "odp",
            "X-ODP-CHANNEL": "mobile",
            "X-SCREEN-TYPE": "MOBILE",
            "Cache-Control": "private, max-age=240",
            "Content-Type": "application/json; charset=UTF-8",
            "Host": "odpapp.asiacell.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/5.0.0-alpha.2"
        }

        if access_token:
            self.headers["Authorization"] = "Bearer " + access_token

        if data:
            self.headers["Content-Length"] = str(len(dumps(data)))
