"""Utils module"""
import requests
from Client.models import Client
from UserProfile.models import UserProfile, Team
import json
from datetime import datetime
from EpicEvents.authentication import read_token
from EpicEvents.settings import BASE_URL


ERROR_MESSAGE = {
    'client_not_existing': 'Impossible de trouver ce client dans la base de données.',
    'user_not_existing': 'Impossible de trouver cet utilisateur dans la base de données.',
    'contract_not_existing': 'Impossible de trouver ce contrat dans la base de données.',
    'event_not_existing': 'Impossible de trouver cet événement dans la base de données.',
    'team_not_existing': 'Impossible de trouver cette équipe dans la base de données.'
}

def input_validated(user_input, empty=False):
    """
    validates user input
    gets user input as string
    returns boolean
    """
    if (user_input == "" or None) and empty is False:
        print("Ce champ ne peut pas être vide")
        return False
    return True


def request_commands(view_url, operation, request_data:dict=None, object_id:int=None, custom_url_filter:str=None):
    """
    roots the command request to the view
    gets :
    - view_url as string,
    - request_data as dict of parameters,
    - (optional) object_id as int to filter on a specific id
    - (optional) custom_url_filter as string to filter on specific field,
    
    note : custom_url_filter is incompatible with object_id
    
    returns a list of dict with the last entry being :
    - 'response_status' being the response.status_code,  
    - 'operation' if success,  
    - 'response_text' if request failed}  
    """
    message_invalid = "Requete non valide"
    request_url = f"{BASE_URL}{view_url}/"
    if object_id is not None:
        request_url = request_url + f'{object_id}/'
    elif custom_url_filter is not None:
        request_url = request_url + f'{custom_url_filter}/'

    headers={"Content-Type": "application/json",}

    # getting the access token from json file then adding to the request header
    access_token = read_token()
    if access_token is not None:
        headers['Authorization'] =  f'Token {access_token["token"]}'

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

    result = []
    if response.text != '':
        result = response.json()

    if isinstance(result, dict):
        result = [result]

    response_data = {}
    response_data['operation'] = operation
    response_data['response_status'] = response.status_code
    if response.status_code // 100 != 2:
        response_data['response_text'] = response.text

    result.append(response_data)

    return result

def print_command_result(title:str="", printable=None):
    """gets a title and an iterable to print"""
    if title != "":
        print(title)

    if printable is None:
        return

    for line in printable:
        print(line)

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
    request_filter = str(f'?{filter_field_name}={filter_field_value}')
    result = request_commands(
        view_url=view_url,
        operation='read',
        custom_url_filter=request_filter
        )
    request_data = result.pop(-1)

    if request_data['response_status'] == 200:
        return result[0]

    return


def get_object_field_from_id(view_url, object_id:int):
    """
    gets view's url as string, object_id as integet
    returns the object found as dict
    """
    result = request_commands(
        view_url=view_url,
        operation='read',
        object_id=object_id
        )
    request_data = result.pop(-1)

    if request_data['response_status'] == 200:
        return result[0]

def get_date_time_from_user()-> datetime:
    """
    Returns formated date-time from user's input
    """
    user_input_list = [
        'year',
        'month',
        'day',
        'hour',
        'minute'
    ]
    user_input_description = {
        'year': 'Année (YYYY): ',
        'month': 'Mois (MM): ',
        'day': 'Jour (DD): ',
        'hour': 'Heure (HH): ',
        'minute': 'Minutes (MM): '
    }

    user_input_result = {}
    result = ''
    for line in user_input_list:
        user_input= input(user_input_description[line])

        user_input_result[line] = user_input
        if result == '':
            pass
        elif line == 'hour':
            result = result + ' '
        elif line == 'minute':
            result = result + ':'
        else:
            result = result + '/'

        if input_validated(user_input=user_input) is False:
            return None

        #reformatting
        if line == 'year':
            user_input = user_input.zfill(4)
        else:
            user_input = user_input.zfill(2)

        result = result + str(user_input)

    try:
        result = datetime.strptime(result+ ":00", '%Y/%m/%d %H:%M:%S')
        return result
    except ValueError:
        return None
