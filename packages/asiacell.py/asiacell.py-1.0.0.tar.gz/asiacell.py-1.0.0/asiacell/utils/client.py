import requests
import json
from time import time
from . import headers
from .helpers import save_auth, load_auth
from .exceptions import handle_exception


class Client:
	def __init__(self, auto_refresh_token: bool = False):
		self.api = "https://odpapp.asiacell.com{}".format
		self.userId = None
		self.username = None
		self.access_token = None
		self.refresh_token = None
		self.handshake_token = None
		self.auto_refresh_token = auto_refresh_token
		self.last_refresh = int(time())
	
	def get_headers(self, data=None):
		return headers.Headers(data).headers

	def set_language(self, language):
		self.api = ("https://odpapp.asiacell.com{}?lang=" + language).format

	def save_auth(self):
		save_auth(
			self.access_token,
			self.refresh_token,
			self.handshake_token,
			self.userId,
			self.username
		)
		headers.access_token = self.access_token
		return True

	def load_auth(self):
		self.auth(load_auth(self.username))
		return True

	def update_token(self):
		if self.refresh_token:
			data = self.auth_post("/api/v1/validate", {"refreshToken": f"Bearer {self.refresh_token}"})
			self.access_token = data["access_token"]
			self.refresh_token = data["refresh_token"]
			self.handshake_token = data["handshake_token"]
			self.last_refresh = int(time())
			self.save_auth()
			return data
		raise handle_exception("No refresh token")
			
	
	def check_refresh_token(self):
		timeout = int(time()) - self.last_refresh
		
		if timeout > 1800:  
			self.update_token()

	def auth(self, validation):
		if not validation:
			raise FileNotFoundError("\"auth.json\" Was not found.")
		headers.access_token = validation["access_token"]
		headers.refresh_token = validation["refresh_token"]
		headers.handshake_token = validation["handshake_token"]
		self.username = validation.get("username")
		self.userId = validation.get("userId")
		self.access_token = headers.access_token
		self.refresh_token = headers.refresh_token
		self.handshake_token = headers.handshake_token
		
	def __compose(self, response):
		try:
			if response.status_code > 300 or not response.json()["success"]:
				return handle_exception(response.json()["message"])
		except json.JSONDecodeError:
			return handle_exception(response.text)
				
		return response.json()

	def __refresh(self):
		if self.auto_refresh_token:
			self.check_refresh_token() 

	def auth_post(self, path: str, data: dict):
		response = requests.post(self.api(path), json=data, headers=self.get_headers(data))
		return self.__compose(response)
	
	def post(self, path: str, data: dict):
		response = requests.post(self.api(path), json=data, headers=self.get_headers(data))
		self.__refresh()
		return self.__compose(response)

	def get(self, path: str):
		response = requests.get(self.api(path), headers=self.get_headers())
		self.__refresh()
		return self.__compose(response)

	def delete(self, path: str):
		response = requests.delete(self.api(path),  headers=self.get_headers())
		self.__refresh()
		return self.__compose(response) 