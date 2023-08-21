from control._callstate import AnonCall
from typing import Literal
from json import loads
from control._base import callcontrol
from resources.exceptions import CallNotActive , CallNotFound



class AnonApi:
    def __init__(self,token:str):
        self.__settoken(token)
    
    def __settoken(self,token:str):
        self._token = token
    
    def create_call(self,to_number:str,
                    from_number:str,
                      callback_url:str):
        __response = str(
            callcontrol(
            "create_call",
            self._token,
            to_num = to_number,
            from_num = from_number,
            callback_url = callback_url
            )
        )
        if loads(__response).get("status","error") == "error":
            raise Exception(f'Error Occured: {loads(__response).get("message","Unknown error occured")}')
        else:
            return AnonCall(loads(__response).get("calluuid"),self)

    def get_call(self,call_uid:str):
        _response = str(
            callcontrol(
            "status",
            self._token,
            calluuid = call_uid
            )
        )
        __response = loads(_response)
        if __response.get("status","error") == "error":
            message = __response.get("message","Unknown error occured")
            if "not found" in message:
                raise CallNotFound(message)
            if "not active" in message:
                raise CallNotActive(message)
            raise Exception(message)
        else:
            return AnonCall(__response.get("calluuid"),self)

    def __repr__(self) -> str:
        return str(AnonCall(self._token , self))