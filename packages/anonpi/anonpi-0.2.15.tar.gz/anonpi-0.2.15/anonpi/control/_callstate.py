from ._base import callcontrol
from json import loads
import typing as t

class AnonCall:
    """AnonCall class for handling call
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        Args:
            calluuid (str): calluuid for handling calls

        Usage:

        >>> call:AnonCall = anonapi.get_call("calluuid")
        >>> call.uuid -> str
        >>> call.playback_start("https://example.com/audio.mp3")
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

    def __init__(self,calluuid:str,cls):
        """AnonCall class for handling call
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        Args:
            calluuid (str): calluuid for handling calls

        Usage:

        >>> call:AnonCall = anonapi.get_call("calluuid")
        >>> call.uuid -> str
        >>> call.playback_start("https://example.com/audio.mp3")
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
        self._calluuid = calluuid
        self._cls = cls
        self._token = cls._token


    def __repr__(self):
        return '<AnonCall calluuid="{}">'.format(self._calluuid)
    
    def __str__(self):
        return '<AnonCall calluuid="{}">'.format(self._calluuid)
    
    @property
    def uuid(self)->str:
        return self._calluuid
    
    def hangup(self):
        _response = str(
            callcontrol(
            "hangup_call",
            self._token,
            calluuid=self._calluuid
            )
        )
        if loads(_response).get("status" , "error") == "error":
            raise Exception(loads(_response).get("message","Unknown error occured"))
        else:
            return None

    def hold(self):
        return callcontrol(
            "hold",
            self._token,
            calluuid=self._calluuid
        )
    
    def unhold(self):
        return callcontrol(
            "unhold",
            self._token,
            calluuid=self._calluuid
        )

    def playback_audio(self,url:str):
        return callcontrol(
            "playback_start",
            self._token,
            calluuid=self._calluuid,
            url=url
        )
    
    def playback_text(self,text:str):
        return callcontrol(
            "playback_text_start",
            self._token,
            calluuid=self._calluuid,
            text=text
        )
    
    def playback_stop(self):
        return callcontrol(
            "playback_stop",
            self._token,
            calluuid=self._calluuid
        )
    
    def record_start(self):
        return callcontrol(
            "record_start",
            self._token,
            calluuid=self._calluuid
        )
    
    def record_stop(self):
        return callcontrol(
            "record_stop",
            self._token,
            calluuid=self._calluuid
        )

    def get_recording(self) -> bytes:
        return callcontrol(
            "record_get",
            self._token,
            calluuid=self._calluuid
        )
    
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
        return callcontrol(
            "gather_audio",
            self._token,
            calluuid=self._calluuid,
            dtmf_count=dtmf_count,
            terminating_digits=terminating_digits,
            audio_url=audio_url
        )
    
    def gather_text(self,
                    dtmf_count:t.Optional[int]=None,
                    terminating_digits:t.Optional[str]=None,
                    text:t.Optional[str]=None):
        return callcontrol(
            "gather_text",
            self._token,
            calluuid=self._calluuid,
            dtmf_count=dtmf_count,
            terminating_digits=terminating_digits,
            text=text
        )          