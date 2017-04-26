from reactivexcomponent.communication.xcSession import XcSession


class XcConnection:

    def create_connection(self, xc_api, server_url, callback):
        self.session = XcSession()
        self.session.init(xc_api, server_url, callback)
