from typing import Literal
from .exceptions import InvalidEndpoint

class AnonEndpoints:
    def __init__(self,endpoint:Literal["create_call",
                                       "hangup_call",
                                       "gather_using_audio",
                                       "gather_using_text",
                                       "playback_text_start",
                                        "playback_audio_start",
                                        "playback_stop",
                                       "unhold",
                                       "hold",
                                       "hangup",
                                       "record_start",
                                       "record_stop"
                                       ,"record_get",
                                       "status"]) -> str:
        """AnonEndpoints class for handling endpoints
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        Returns:
            str: endpoint url with base url
        """
        self._endpoint = endpoint
        self.base_url = "http://68.183.93.228:5000/api/v1/"
        self._endpoints = {
            "create_call":"call/create",
            "hangup_call":"call/hangup",
            "gather_using_audio":"call/gather/audio",
            "gather_using_text":"call/gather/text",
            "hold":"call/hold",
            "hangup":"call/hangup",
            "unhold":"call/unhold",
            "record_start":"call/record/start",
            "record_stop":"call/record/stop",
            "record_get":"call/record/get",
            "playback_audio_start":"call/playback/start/audio",
            "playback_text_start":"call/playback/start/text",
            "playback_stop":"call/playback/stop",
            "status":"call/status"

        }

    def __repr__(self)-> str:
        if self._endpoint not in self._endpoints:
            raise InvalidEndpoint(f"Invalid endpoint {self._endpoint}")
        return self.base_url+self._endpoints[self._endpoint]
