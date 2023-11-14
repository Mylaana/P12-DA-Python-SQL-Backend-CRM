"""Utils module"""
import requests
from Client.models import Client
from UserProfile.models import UserProfile, Team


BASE_URL = "http://localhost:8000/"

def input_validated(user_input, empty=False):
    """
    validates user input
    gets user input as string
    returns boolean
    """
    if user_input == "" and empty is False:
        print("Ce champs ne peut pas être vide")
        return False
    return True


def request_commands(view_url, operation, request_data:dict=None, object_id:int=None, object_name:str=None):
    """
    roots the command request to the view
    object_name should be a string and will be used only if object_id is none.
    """
    message_invalid = "Requete non valide"
    request_url = f"{BASE_URL}{view_url}/"
    if object_id is not None:
        request_url = request_url + f'{object_id}/'

    headers={"Content-Type": "application/json",}

    if operation == "read":
        response = requests.get(url=request_url, json=request_data, headers=headers, timeout=5000)

    elif operation == "create":
        response = requests.post(url=request_url, json=request_data, headers=headers, timeout=5000)

    elif operation == "delete":
        # force id filter to be specified
        if object_id is None:
            return message_invalid
        print(request_data)
        print(object_id)
        print(request_url)
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


def get_ee_contact_id(username:str):
    """gets username returns contact id"""
    result = UserProfile.objects.filter(username=username).first()

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
    """gets client name returns id"""
    result = Client.objects.filter(name=client_name).first()

    if result is None:
        return None

    return result.id

def get_team_id(name:str):
    """gets name returns id"""
    result = Team.objects.filter(name=name).first()

    if result is None:
        return None

    return result.id

def get_team_name(object_id:str):
    """gets name returns id"""
    result = Team.objects.filter(id=object_id).first()

    if result is None:
        return None

    return result.name