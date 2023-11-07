"""Utils module"""
import requests
from rest_framework.response import Response
from rest_framework import status
from Client.models import Client
from UserProfile.models import UserProfile


BASE_URL = "http://localhost:8000/"

def input_validated(user_input, empty=True):
    """
    validates user input
    gets user input as string
    returns boolean
    """
    if user_input == "" and empty is False:
        print("Ce champs ne peut pas être vide")
        return False
    return True


def request_commands(view_url, operation, request_data:dict=None, id:int=None):
    """roots the command request to the view"""
    message_invalid = "Requete non valide"
    request_url = f"{BASE_URL}{view_url}/"
    if id is not None:
        request_url = request_url + f'{id}/'
    headers={"Content-Type": "application/json",}

    if operation == "read":
        response = requests.get(url=request_url, json=request_data, headers=headers, timeout=5000)

    elif operation == "create":
        response = requests.post(url=request_url, json=request_data, headers=headers, timeout=5000)

    elif operation == "delete":
        # force id filter to be specified
        if id is None:
            return message_invalid

        response = requests.delete(url=request_url, headers=headers, timeout=5000)

    elif operation == "update":
        response = requests.patch(url=request_url, json=request_data, headers=headers, timeout=5000)
    else:
        return message_invalid

    if response.status_code != 200:
        return response.text

    if operation == "read":
        return response.json()
    else:
        return operation

def print_command_result(title:str="", printable=None):
    """gets a title and an iterable to print"""
    if title != "":
        print(title)

    if printable is None:
        return

    for line in printable:
        print(line)


def get_ee_contact_id(contact_name:str):
    """gets contact name returns contact id"""
    result = UserProfile.objects.filter(username=contact_name).first()

    if result is None:
        return None

    return result.id

def get_ee_contact_name(contact_id:int):
    """gets user id returns username"""
    result = UserProfile.objects.filter(id=contact_id).first()

    if result is None:
        return None

    return result.username

def get_ee_client_id(client_name:str):
    """gets username returns user id"""
    result = Client.objects.filter(name=client_name).first()

    if result is None:
        return None

    return result.id
