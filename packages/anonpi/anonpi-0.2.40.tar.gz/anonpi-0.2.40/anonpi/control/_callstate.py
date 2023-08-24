from ._base import callcontrol
from json import loads
import typing as t
from ..resources.exceptions import CallNotActive , CallNotFound , TokenRequired , InvalidParameter
from ._recording import Recording

class AnonCall:
    """AnonCall class for handling call
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        Args:
            calluuid (str): calluuid for handling calls

        Usage:

        >>> call:AnonCall = anonapi.get_call("calluuid")
        >>> call.uuid -> str
        >>> call.playback_audio("https://example.com/audio.mp3")
        >>> call.playback_text() -> None
        >>> call.playback_stop() -> None
        >>> call.hangup() -> None
        >>> call.status() -> bool
        >>> call.hold() -> None
        >>> call.unhold() -> None
        >>> call.record_start() -> None
        >>> call.record_stop() -> None
        >>> call.get_recording() -> bytes

        Raises:
            Exception: If calluuid is not valid
        """

    def __init__(self,**d):
        """AnonCall class for handling call
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        Args:
            calluuid (str): calluuid for handling calls

        Usage:

        >>> call:AnonCall = anonapi.get_call("calluuid")
        >>> call.uuid -> str
        >>> call.playback_audio("https://example.com/audio.mp3")
        >>> call.playback_stop() -> None
        >>> call.hangup() -> None
        >>> call.status() -> bool
        >>> call.hold() -> None
        >>> call.unhold() -> None
        >>> call.record_start() -> None
        >>> call.record_stop() -> None
        >>> call.get_recording() -> bytes

        Raises:
            Exception: If calluuid is not valid
        """
        self._calluuid = d.get("calluuid")
        self._token = d.get("token")
        if not self._calluuid:
            raise InvalidParameter("calluuid is required to create AnonCall instance")
        if not self._token:
            raise TokenRequired("token is required to create AnonCall instance")


    def __repr__(self):
        return '<AnonCall calluuid="{}">'.format(self._calluuid)
    
    def __str__(self):
        return '<AnonCall calluuid="{}">'.format(self._calluuid)
    
    @property
    def uuid(self)->str:
        return self._calluuid
    
    def hangup(self):
        __  =  str(
            callcontrol(
            "hangup_call",
            self._token,
            calluuid=self._calluuid
            )
        )
        return None

    def hold(self):
        __ =  str(callcontrol(
            "hold",
            self._token,
            calluuid=self._calluuid
        ))
        return None
    
    def unhold(self):
        __ =  str(callcontrol(
            "unhold",
            self._token,
            calluuid=self._calluuid
        ))
        return None

    def playback_audio(self,audio_url:str):
        __ =  str(callcontrol(
            "playback_audio_start",
            self._token,
            calluuid=self._calluuid,
            audio_url = audio_url
        ))
        return None
    
    def playback_text(self,text:str):
        __  = str(callcontrol(
            "playback_text_start",
            self._token,
            calluuid=self._calluuid,
            text=text
        ))
        return None
    
    def playback_stop(self):
        __  =  str(callcontrol(
            "playback_stop",
            self._token,
            calluuid=self._calluuid
        ))
        return None
    
    def record_start(self):
        __ =  str(callcontrol(
            "record_start",
            self._token,
            calluuid=self._calluuid
        ))
        return None
    

    def record_stop(self):
        __ =  str(callcontrol(
            "record_stop",
            self._token,
            calluuid=self._calluuid
        ))
        return None


    def get_recording(self) -> Recording:
        __ =  loads(str(callcontrol(
            "record_get",
            self._token,
            calluuid=self._calluuid
        )))
        return Recording(**__)


    
    def pause_recording(self):
        return callcontrol(
            "record_pause",
            self._token,
            calluuid=self._calluuid
        )
    
    def resume_recording(self):
        return callcontrol(
            "record_resume",
            self._token,
            calluuid=self._calluuid
        )

    def status(self):
        return callcontrol(
            "status",
            self._token,
            calluuid=self._calluuid
        ).get("status",False)
    
    def gather_audio(self,
                     *,
                     dtmf_count:t.Optional[int]=None,
                     terminating_digits:t.Optional[str]=None,
                     audio_url:t.Optional[str]=None):
        return str(callcontrol(
            "gather_using_audio",
            self._token,
            calluuid=self._calluuid,
            dtmf_count=dtmf_count,
            terminating_digits=terminating_digits,
            audio_url=audio_url
        ))
    
    def gather_text(self,
                    *,
                    dtmf_count:t.Optional[int]=None,
                    terminating_digits:t.Optional[str]=None,
                    text:t.Optional[str]=None):
        return callcontrol(
            "gather_using_audio",
            self._token,
            calluuid=self._calluuid,
            dtmf_count=dtmf_count,
            terminating_digits=terminating_digits,
            text=text
        )   

