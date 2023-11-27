import os
from getpass import getpass
import json
import requests
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from EpicEvents.settings import BASE_DIR, BASE_URL


class CustomObtainAuthToken(ObtainAuthToken):
    """handles the token generation"""
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        return Response({'error': 'Login failed'}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # deleting the token from database
        request.auth.delete()
        return Response({'detail': 'Déconnexion réussie.'}, status=status.HTTP_200_OK)

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
        print(f"response status test: {response.text}")
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
    #checks if file exists
    if os.path.isfile(str(BASE_DIR) + "/" + TOKEN_FILENAME) is False:
        return None

    with open(TOKEN_FILENAME, 'r', encoding='utf-8') as json_file:
        loaded_data = json.load(json_file)

    return loaded_data

def request_logout():
    """logs out the current user"""
    access_token = read_token()
    headers={
        "Content-Type": "application/json",
        "Authorization": f"Token {access_token['token']}",
             }
    response = requests.post(url=BASE_URL + '/logout/', headers=headers, timeout=5000)
    return response

