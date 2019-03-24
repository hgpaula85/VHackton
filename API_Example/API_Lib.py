import requests
import json
import os.path
from datetime import date
from random import randint

host = "https://mockapi-home.com/%s"  # Global variable for host
endpoint = "ep1/as_endpoint/"  # Global variable for endpoint


# List of cards - Read from CSV and build it to a list
def build_cards_list():
    my_path = os.path.abspath(os.path.dirname(__file__))
    cards_file = os.path.join(my_path, "data/cards.txt")

    with open(cards_file) as temp:
        list_reader = temp.read().splitlines()  # To remove new line char
        cards_list = []
        for line in list_reader:
            cards_list.append(line)

    cards_list = list(map(int, cards_list))

    return cards_list

# Return the AMOUNT parameter always as a multiple of 10


def return_amount():

    my_amount = randint(1, 99) * 100
    while my_amount % 100 > 0:
        my_amount = randint(1, 99) * 100

    return my_amount

# Class to build JSON requests


class CreatingRequests(object):
    """
    This class has the necessary methods to build JSON requests
    """

    @staticmethod
    def uri_auth():
        """
        This method combines Host and Endpoint to build URI
        :param str endpoint: static endpoint
        :return str uri: URI
        """
        uri = host % endpoint
        return uri

    def header(self):
        """
        Build Header with static authentication token
        :return str header: Header necessary to build JSON request
        """
        header = {
            "Content-Type": "application/json",
            "Authorization": "basic MTIzNDEwODg6NDkxM2JiMjRhMDI4NDk1NGJlNzJjNDI1OGUyMjliODY="
        }
        return header

    def payload_auth(self, capture, kind, cardholdername, installments, cardnumber):
        """
        Build the payload (body) for Authorization or Pre-Authorization
        :param str capture: true (for Authorization) ou false (for pre-authorization)
        :param str kind: credit or debit
        :param str cardholdername: Cardholder name
        :param int installments: 00 to 99
        :param int cardnumber: Card number
        :return str payload: Body necessary to build JSON request
        """

        payload = {
            "capture": capture,
            "Kind": kind,
            "reference": randint(11111111, 99999999),
            "amount": return_amount(),
            "cardholderName": cardholdername,
            "installments": installments,
            "softdescriptor": "legal",
            "cardNumber": cardnumber,
            "expirationMonth": randint(1, 12),
            "expirationYear": randint(date.today().year, date.today().year + 4),
            "SecurityCode": randint(123, 999),
            "subscription": "1",
            "origin": 1,
        }
        return payload

    def send_request(self, uri, headers, payload, method):
        """
        Post the JSON request
        :param str uri: URI
        :param str headers: Header
        :param str payload: Payload (or Body)
        :param str method: Method to create request (Ex: GET, POST, PUT...)
        :return str response: Response to the request
        """
        request = requests.Session()

        if method == "PUT":
            response = request.put(uri, data=json.dumps(payload), headers=headers)
        else:
            response = request.post(uri, data=json.dumps(payload), headers=headers)

        return response

    def uri_confirm(self, tid):
        """
        This method combines URI and Transaction ID to build confirmation URI
        :param str endpoint: Endpoint
        :param int tid: Transaction ID (Created on pre-authorization
        :return int uri: URI
        """
        uri = host % endpoint
        uri = uri + str(tid)
        return uri

    def payload_confirm(self, amount):
        """
        Build the payload (body) for Confirmation
        :param int amount: Transaction Amount
        :return str payload: Body necessary to build JSON request
        """

        payload = {
            "amount": amount,
        }
        return payload
