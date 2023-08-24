from typing import Literal
from ._api import apibaserequest
from resources._endpoints import AnonEndpoints
from json import loads , dumps
from resources.exceptions import CallNotActive , CallNotFound


[
    "create_call",
    "hangup_call",
    "status"
]


class callcontrol:
    def __init__(self, event: Literal["create_call",
                                       "hangup_call",
                                       "gather_aduio",
                                       "gather_text",
                                       "playback_text_start",
                                        "playback_audio_start",
                                        "playback_stop",
                                       "unhold",
                                       "hold",
                                       "hangup",
                                       "record_start",
                                       "record_stop"
                                       ,"record_get",
                                       "status"], token: str, **kwargs):
        self._kwargs = kwargs
        self._token = token
        self._event = event

    def _check_call_status(self):
        calluuid = self._kwargs["calluuid"]
        return apibaserequest(
            "get",
            AnonEndpoints("status"),
            self._token,
            calluuid=calluuid
        )


    def __repr__(self):
        if self._event == "record_get":
            __D =  loads(str(apibaserequest(
                "get",
                AnonEndpoints("record_get"),
                self._token,
                calluuid=self._kwargs["calluuid"]
            )))
            if __D.get("status","error") == "error":
                raise Exception(__D.get("message","Unknown error occured"))
            else:
                return __D
            
        if self._event == "status":
            return str(self._check_call_status())
        else:
            __checkstatus = self._check_call_status()
            if __checkstatus.get("status", "error") == "error":
                message = __checkstatus.get("message","Unknown error occured")
                if "not found" in message:
                    raise CallNotFound(message)
                if "not active" in message:
                    raise CallNotActive(message)
                raise Exception(message)
            else:
                return str(apibaserequest(
                    "post",
                    AnonEndpoints(self._event),
                    self._token,
                    **self._kwargs
                ))
