from reactivexcomponent.communication.xc_connection import XcConnection


class XcomponentAPI:
    def __init__(self):
        self.connection = None

    def create_session(self, xc_api, server_url, callback):
        self.connection = XcConnection()
        self.connection.create_connection(xc_api, server_url, callback)
