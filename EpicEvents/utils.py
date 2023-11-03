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

    request_url = f"{BASE_URL}{view_url}/"
    headers={"Content-Type": "application/json",}

    if operation == "get":
        response = requests.get(url=request_url, json=request_data, headers=headers, timeout=5000)

    elif operation == "create":
        response = requests.post(url=request_url, json=request_data, headers=headers, timeout=5000)

    elif operation == "delete":
        response = requests.delete(url=request_url, json=request_data, headers=headers, timeout=5000)

    elif operation == "put":
        response = requests.patch(url=request_url, json=request_data, headers=headers, timeout=5000)
    else:
        return "Invalid Request"

    if response.status_code != 200:
        return response.text

    if operation == "get":
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
