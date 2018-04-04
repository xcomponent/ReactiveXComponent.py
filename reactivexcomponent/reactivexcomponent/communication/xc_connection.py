from typing import Callable, Any
from reactivexcomponent.communication.xc_session import XcSession


class XcConnection:
    def __init__(self) -> None:
        pass

    def create_connection(self, xc_api: str, server_url: str, callback: Callable[[Any, Any], None]) -> None:
        self.session: XcSession = XcSession()
        self.session.init(xc_api, server_url, callback)
