from .control._callstate import AnonCall
from json import loads
from .control._base import callcontrol
from .resources.exceptions import CallNotActive , CallNotFound , TokenRequired



class AnonApi:
    """ Base class AnonApi create and get calls
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        ```python
        from anonpi import AnonApi

        api = AnonApi("token")
        call = api.create_call("to_number","from_number","callback_url")
        ```
    """
    def __init__(self,token:str=None):
        if not token:
            raise TokenRequired("Token is required to create AnonApi instance, if you don't have one, get it from https://anonpi.co")
        else:
            self.__settoken(token)

    def __settoken(self,token:str):
        self._token = str(token)
    
    def create_call(self,to_number:str,
                    from_number:str,
                      callback_url:str):
        __response = str(
            callcontrol(
            "create_call",
            self._token,
            to_number = to_number,
            from_number = from_number,
            callback_url = callback_url
            )
        )
        if loads(__response).get("status","error") == "error":
            raise Exception(f'Error Occured: {loads(__response).get("message","Unknown error occured")}')
        else:
            return AnonCall(calluuid=loads(__response).get("calluuid"),token=self._token)

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
            raise Exception(f'Error Occured: {message}')
        else:
            return AnonCall(calluuid=__response.get("calluuid"),token=self._token)

    def __repr__(self) -> str:
        return str("<{}>".format(self.__class__.__name__))