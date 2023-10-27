from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from getpass import getpass
import requests


AUTH_URL = "http://localhost:8000/token-auth/"

class Command(BaseCommand):

    help = 'Affiche la liste des utilisateurs enregistrés dans la base de données'

    def handle(self, *args, **options):
        username = input("enter username:")
        password = getpass("enter password:")

        auth_data = {
            'username': username,
            'password': password
            }
        
        response = requests.post(url=AUTH_URL, data=auth_data)
        #user = authenticate(username=username, password=password)
        print (response.status_code)
        if response.status_code == 200:
            print(f"token : {response.json().get('token')}")

    def request_get_token(self):
        pass