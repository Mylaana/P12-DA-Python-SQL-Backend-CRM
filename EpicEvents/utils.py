"""Utils module"""
import requests
from rest_framework.response import Response
from rest_framework import status


BASE_URL = "http://localhost:8000/"

def input_validation(user_input, empty=True):
    """
    validates user input
    gets user input as string
    returns boolean
    """
    if user_input == "" and empty is False:
        print("Ce champs ne peut pas être vide")
        return False


def request_commands(view_url, operation, request_data:dict=None):
    """roots the command request to the view"""
    message = "Une erreur s'est produite"


    request_url = f"{BASE_URL}{view_url}/"
    headers={"Content-Type": "application/json",}

    if operation == "read":
        response = requests.get(url=request_url, json=request_data, headers=headers, timeout=5000)
        message = ""
    elif operation == "create":
        response = requests.post(url=request_url, json=request_data, headers=headers, timeout=5000)
        message = "objet créé avec succes."

    print(message)
    if response.status_code != 200:
        print(response.text)


    if operation == "read":
        return response.json()
