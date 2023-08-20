"""
Copyright (c) Jordan Maxwell. All rights reserved.
See LICENSE file in the project froot for full license information.
"""

import json
from flask import jsonify

class AliceServerDTO(object):
    """
    Represents a DTO object that is sent to and from the server
    """

    def is_valid(self) -> bool:
        """
        Returns true if the DTO is valid
        """

        raise NotImplementedError("%s does not implement is_valid" % self.__class__.__name__)

    def to_dict(self) -> dict:
        """
        Returns this DTO as a dictionary object
        """

        raise NotImplementedError("%s does not imlpement to_dict" % self.__class__.__name__)
    
    def to_json(self) -> str:
        """
        Converts the DTO object to a JSON string
        """

        return json.dumps(self.to_dict(), indent=4, sort_keys=True)
        

    def __dict__(self) -> dict:
        """
        Converts the DTO object to a dictionary
        """

        return self.to_dict()

    def __str__(self) -> str:
        """
        Converts the DTO object to a JSON string
        """

        return self.to_json()
    
    def __repr__(self) -> str:
        """
        Converts the DTO object to a JSON string
        """

        return self.to_json()
    
    def __eq__(self, other) -> bool:
        """
        Compares two DTO objects
        """

        return self.to_dict() == other.to_dict()
    
    def __ne__(self, other) -> bool:
        """
        Compares two DTO objects
        """

        return self.to_dict() != other.to_dict()
    
    @classmethod
    def from_dict(cls: object, dict: dict) -> object:
        """
        Builds the DTO from a dictionary
        """

        return cls(**dict)
    
    @classmethod
    def from_json(cls: object, json: str) -> object:
        """
        Builds the DTO from a JSON string
        """

        return cls.from_dict(json.loads(json))

    @classmethod
    def from_reqeuest(cls: object, request: object) -> object:
        """
        Builds the DTO from a Flask request
        """

        return cls.from_dict(request.json)
    
    def to_response(self, code: int = 200) -> tuple:
        """
        Transforms the DTO into a Flask response
        """

        return jsonify(self.to_dict()), 200