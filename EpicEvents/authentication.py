from getpass import getpass
import json
import requests
from EpicEvents.settings import BASE_DIR
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken

class CustomObtainAuthToken(ObtainAuthToken):
    """handles the token generation"""
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        return Response({'error': 'Login failed'}, status=status.HTTP_400_BAD_REQUEST)


AUTH_URL = "http://localhost:8000/token-auth/"
TOKEN_FILENAME = "credentials.json"

def request_get_token():
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

def write_token(auth_data):
    """writes token in credential json file"""

    # removes password from data to be written
    write_data = auth_data
    write_data['password'] = ''

    with open(str(BASE_DIR) + "/" + TOKEN_FILENAME, 'w', encoding='utf-8') as json_file:
        json.dump(auth_data, json_file, indent=4)

def read_token() -> dict:
    """loads token from credential json file"""

    with open(TOKEN_FILENAME, 'r', encoding='utf-8') as json_file:
        loaded_data = json.load(json_file)

    return loaded_data
