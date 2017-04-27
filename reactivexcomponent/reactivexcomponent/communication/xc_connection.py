from reactivexcomponent.communication.xc_session import XcSession


class XcConnection:

    def __init__(self):
        self.session = None

    def create_connection(self, xc_api, server_url, callback):
        self.session = XcSession()
        self.session.init(xc_api, server_url, callback)
