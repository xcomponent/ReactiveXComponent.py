from reactivexcomponent.communication.xc_connection import XcConnection
from typing import Callable, Any

class XcomponentAPI:
    def __init__(self) -> None:
        pass

    def create_session(self, xc_api: str, server_url: str, callback: Callable[[Any, Any], None]) -> None:
        self.connection = XcConnection()
        self.connection.create_connection(xc_api, server_url, callback)
