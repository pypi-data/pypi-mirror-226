"""
Copyright (c) Jordan Maxwell. All rights reserved.
See LICENSE file in the project froot for full license information.
"""

import requests

from alice.client.models import llm

ALICE_SERVER_URL = "http://localhost:8080"

class AliceAPIException(Exception):
    """
    Exception raised when there is an issue with the Alice serverAPI.
    """

    error_code: int
    error_type: str
    error_message: str

    def __init__(self, response: requests.Response):
        """
        Constructs an AliceAPIException from the given requests response.
        """

        try:
            response_data = response.json()
        except:
            response_data = {}

        self.error_code = response_data.get("error_code", 500)
        self.error_type = response_data.get("error_type", "InternalError")
        self.error_message = response_data.get("error_message", "An unknown error occurred.")

        super().__init__("(%s): %s" % (self.error_type, self.error_message))

def _check_for_api_exception(response: requests.Response) -> None:
    """
    Checks for an API exception and raises it if it exists.
    """

    if response.status_code != 200:
        raise AliceAPIException(response)
    
def is_server_healthy() -> bool:
    """
    Checks if the Alice server is healthy.
    """

    response = requests.get("%s/health" % ALICE_SERVER_URL)
    _check_for_api_exception(response)

    return response.text == "OK"

def execute_llm_request(request: llm.AliceLLMExecuteRequest) -> str:
    """
    Executes a LLM request against the Alice server.
    """

    response = requests.post("%s/llm/execute" % ALICE_SERVER_URL, json=request.to_dict())
    _check_for_api_exception(response)

    return response.json()["result"]