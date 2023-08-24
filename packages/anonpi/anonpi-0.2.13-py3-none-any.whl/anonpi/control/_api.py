from typing import Literal
from requests import request
from json import dumps

class apibaserequest:
    def __init__(self,menthod:Literal["get","post","delete","patch"],url:str,token:str,**data):
        self._method = menthod
        self._url = url
        self._token = token
        self._data = data

    def __repr__(self):
        _headers = {
            "Authorization": self._token
        }
        res = request(
            method=self._method,
            url=self._url,
            json= self._data,
            headers=_headers
        )
        try:
            return dumps(res.json())
        except:
            raise Exception("Server side error occured")





    