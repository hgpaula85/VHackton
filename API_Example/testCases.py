import random
import unittest
from API_Example.API_Lib import build_cards_list
from API_Example.API_Lib import CreatingRequests


# Class to build test cases
class APITestCases(unittest.TestCase):
    """
    This class contains the test cases
    """

    # To validate pre-authorization transaction with 0 installments
    def test_PreAuthorization_with_no_Installments(self):

        # Arrange - define endpoint, headers and payload
        card = random.choice(build_cards_list())
        full_request = CreatingRequests()
        req_uri = full_request.uri_auth()
        req_header = full_request.header()
        req_payload = full_request.payload_auth("false", "credit", "Test case 001", 00, card)

        # Act - send the request
        pre_auth_response = full_request.send_request(req_uri, req_header, req_payload, "POST").json()

        # Assert
        return_message = "Expected: 00 - Found: %d" % int(pre_auth_response["returnCode"])
        self.assertEqual(0, int(pre_auth_response["returnCode"]), return_message)
        print(return_message)

    # To validate pre-authorization confirmation
    def test_preAuthorization_Confirmation(self):

        # Arrange - define endpoint, headers and payload
        card = random.choice(build_cards_list())
        full_request = CreatingRequests()
        req_uri = full_request.uri_auth()
        req_header = full_request.header()
        req_payload = full_request.payload_auth("false", "credit", "Test case 002", 00, card)

        # Act - send the request
        pre_auth_response = full_request.send_request(req_uri, req_header, req_payload, "POST").json()

        if pre_auth_response["returnCode"] == "00":
            full_request = CreatingRequests()
            req_uri = full_request.uri_confirm(pre_auth_response["tid"])
            req_header = full_request.header()
            req_payload = full_request.payload_confirm(pre_auth_response["amount"])

            print(req_uri)
            print(req_header)
            print(req_payload)

            conf_response = full_request.send_request(req_uri, req_header, req_payload, "PUT").json()
            print(conf_response)

        else:
            conf_response = {"returnCode": 99}

        # Assert
        return_message = "Expected: 00 - Found: %d" % int(conf_response["returnCode"])
        self.assertEqual(0, int(pre_auth_response["returnCode"]), return_message)
        print(return_message)

if __name__ == "__main__":
    unittest.main()
