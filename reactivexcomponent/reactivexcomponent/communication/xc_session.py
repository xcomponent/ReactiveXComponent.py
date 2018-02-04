import ssl
import websocket as WebSocket
from rx.subjects import Subject
from reactivexcomponent.communication.publisher import Publisher
from reactivexcomponent.communication.subscriber import Subscriber
from reactivexcomponent.configuration.api_configuration import APIConfiguration


def remove_element(table, element):
    if element in table:
        del table[table.index(element)]
    else:
        raise Exception("Element to remove not found")

SUCCESS = None


class XcSession:

    def __init__(self):
        self.websocket = None
        self.xc_api = ""
        self.configuration = None
        self.reply_publisher = None
        self.stream = Subject()
        self.publishers = []
        self.subscribers = []
        
    def init(self, xc_api, server_url, callback):
        self.xc_api = xc_api
        self.websocket = WebSocket.WebSocketApp(server_url)
        self.configuration = APIConfiguration(self.xc_api)
        self.reply_publisher = Publisher(self.configuration, self.websocket)
        self.publishers.append(self.reply_publisher)

        def on_message(websocket, message):
            self.stream.on_next(message)

        def on_open(websocket):
            callback(SUCCESS, self)

        def on_error(websocket, error):
            callback(error, None)

        def on_close(websocket):
            print('### session %s closed ###' % server_url)

        self.websocket.on_message = on_message
        self.websocket.on_open = on_open
        self.websocket.on_error = on_error
        self.websocket.on_close = on_close

        self.websocket.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})

    def create_publisher(self):
        configuration = APIConfiguration(self.xc_api)
        publisher = Publisher(configuration, self.websocket)
        self.publishers.append(publisher)
        return publisher

    def create_subscriber(self):
        configuration = APIConfiguration(self.xc_api)
        subscriber = Subscriber(configuration, self.websocket, self.stream, self.reply_publisher)
        self.subscribers.append(subscriber)
        return subscriber

    def dispose_subscriber(self, subscriber):
        remove_element(self.subscribers, subscriber)

    def dispose_publisher(self, publisher):
        remove_element(self.publishers, publisher)

    def dispose_publishers_subscribers(self):
        self.publishers = [self.dispose_publisher(publisher) for publisher in self.publishers]
        self.subscribers = [self.dispose_subscriber(subscriber) for subscriber in self.subscribers]

    def close_session(self):
        self.dispose_publishers_subscribers()
        self.websocket.close()
