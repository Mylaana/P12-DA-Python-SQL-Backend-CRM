"""Utils module"""
import requests
from Client.models import Client
from UserProfile.models import UserProfile, Team
import json


BASE_URL = "http://localhost:8000/"


ERROR_MESSAGE = {
    'client_not_existing': 'Impossible de trouver ce client dans la base de données.',
    'user_not_existing': 'Impossible de trouver cet utilisateur dans la base de données.',
    'contract_not_existing': 'Impossible de trouver ce contrat dans la base de données.',
    'event_not_existing': 'Impossible de trouver cet événement dans la base de données.'
}

def input_validated(user_input, empty=False):
    """
    validates user input
    gets user input as string
    returns boolean
    """
    if user_input == "" and empty is False:
        print("Ce champ ne peut pas être vide")
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

def get_object_from_field_name(view_url, filter_field_name:str, filter_field_value):
    """
    gets a veiw and a field_name
    returns object if found
    """
    if filter_field_name == 'id':
        return get_object_field_from_id(
            view_url=view_url,
            object_id=filter_field_value
            )
    else:
        return get_object_from_any_field(
            view_url=view_url,
            filter_field_name=filter_field_name,
            filter_field_value=filter_field_value
        )

def get_object_from_any_field(view_url, filter_field_name:str, filter_field_value):
    """
    gets view, a field_name from an object and it's value for filtering
    returns the object found
    """
    request_result = request_commands(
        view_url=view_url,
        operation='read',
        object_id=None
        )

    for item in request_result:
        if item[filter_field_name] == filter_field_value :
            return item


def get_object_field_from_id(view_url, object_id:int):
    """
    gets view, object_id
    returns the object found
    """
    return request_commands(
        view_url=view_url,
        operation='read',
        object_id=object_id
        )
