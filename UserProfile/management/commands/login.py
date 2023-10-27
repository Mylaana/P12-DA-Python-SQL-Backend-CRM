from django.core.management.base import BaseCommand
from getpass import getpass
import requests
import json
from EpicEvents.settings import BASE_DIR

AUTH_URL = "http://localhost:8000/token-auth/"
TOKEN_FILENAME = "credentials.json"

class Command(BaseCommand):

    def handle(self, *args, **options):
        """handles 'login' command"""

        #check if token exists
        #check_if_token()
        auth_data = self.request_get_token()
        if auth_data['token'] is not None:
            print(f"Vous êtes authentifié, bienvenue {auth_data['username']}")
            self.write_token(auth_data)


    def request_get_token(self):
        """asks user for credentials and returns token as string
        returns none if could not authenticate"""
        username = input("enter username:")
        password = getpass("enter password:")

        auth_data = {
            'username': username,
            'password': password,
            'token': None
            }

        response = requests.post(url=AUTH_URL, data=auth_data, timeout=5000)

        if response.status_code != 200:
            print("Authentification impossible")
            print(f"response status code: {response.status_code}")
            return auth_data

        auth_data['token'] = response.json().get('token')
        return auth_data

    def write_token(self, auth_data):
        """writes token in credential json file"""

        #removes password from data to be written
        write_data = auth_data
        write_data['password'] = ''

        with open(str(BASE_DIR) + "/" + TOKEN_FILENAME, 'w') as json_file:
            json.dump(auth_data, json_file, indent=4)

    def load_token(self):
        """loads token from credential json file"""

        with open(TOKEN_FILENAME, 'r') as json_file:
            loaded_data = json.load(json_file)

        return loaded_data
