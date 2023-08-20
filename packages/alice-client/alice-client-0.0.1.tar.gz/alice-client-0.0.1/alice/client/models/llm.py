"""
Copyright (c) Jordan Maxwell. All rights reserved.
See LICENSE file in the project froot for full license information.
"""

from alice.client.models import dto

class AliceLLMExecuteRequest(dto.AliceServerDTO):
    """
    """

    def __init__(self, location: str, speaker: str, input: str, history=[]):
        """
        """

        self.location = location
        self.speaker = speaker
        self.input = input
        self.history = history

    def is_valid(self) -> bool:
        """
        Returns true if the DTO is valid
        """

        return self.location is not None and self.speaker is not None and self.input is not None
    
    def to_dict(self) -> dict:
        """
        Returns this DTO as a dictionary object
        """
            
        return {
            "location": self.location,
            "speaker": self.speaker,
            "input": self.input
        }