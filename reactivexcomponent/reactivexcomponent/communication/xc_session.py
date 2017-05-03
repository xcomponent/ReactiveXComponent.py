import ssl
import websocket as WebSocket
from reactivexcomponent.communication.publisher import Publisher
from reactivexcomponent.configuration.api_configuration import APIConfiguration as configuration

SUCCESS = None

class XcSession:

    def __init__(self):
        self.websocket = None
        self.configuration = configuration
        self.xc_api = ""

    def init(self, xc_api, server_url, callback):
        self.xc_api = xc_api
        self.websocket = WebSocket.WebSocketApp(server_url)

        # pylint: disable=unused-argument
        def on_open(websocket):
            callback(SUCCESS, self)

        def on_error(websocket, error):
            callback(error, None)

        def on_close(websocket):
            print('### session %s closed ###' % server_url)

        self.websocket.on_open = on_open
        self.websocket.on_error = on_error
        self.websocket.on_close = on_close

        self.websocket.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})

    def create_publisher(self):
        configuration = self.configuration(self.xc_api)
        configuration.get_xml_content()
        publisher = Publisher(configuration, self.websocket)
        return publisher
