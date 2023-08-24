import requests

class Recording(object):
    def __init__(self,**d):
        self.__URL = d.get("url")
    
    @property
    def url(self):
        return self.__URL
    
    @property
    def audio_data(self):
        return requests.get(self.__URL).content

    def __repr__(self):
        return f"<Recording url={self.__URL}>"
           