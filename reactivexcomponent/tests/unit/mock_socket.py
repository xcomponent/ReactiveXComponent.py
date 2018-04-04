
# Mocking server


class MockWebSocket:

    def __init__(self, server_url):
        self.server_url = server_url
        self.server = None
        self.on_open = None
        self.on_message = None
        self.on_close = None
        self.on_error = None


class MockServer:
    def __init__(self, server_url):
        self.server_url = server_url
        self.client = None

    def init(self):
        if self.client.server_url == self.server_url:
            self.client.on_open()
        else:
            self.client.on_error()
# create_mock_server
