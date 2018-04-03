import ssl
import websocket as WebSocket
from typing import List, Any, Callable
from rx.subjects import Subject
from reactivexcomponent.communication.publisher import Publisher
from reactivexcomponent.communication.subscriber import Subscriber
from reactivexcomponent.configuration.api_configuration import APIConfiguration

def remove_element(table: List[Any], element: Any) -> List[Any]:
    if element in table:
        del table[table.index(element)]
    else:
        raise Exception("Element to remove not found")

SUCCESS = None

class XcSession:
    def __init__(self) -> None:
        self.stream = Subject()
        self.publishers: List[Publisher] = []
        self.subscribers: List[Subscriber] = []

    def init(self, xc_api: str, server_url: str, callback: Callable[[Any, Any], None]) -> None:
        self.xc_api = xc_api
        self.websocket: WebSocket.WebSocketApp = WebSocket.WebSocketApp(server_url)
        self.configuration = APIConfiguration(self.xc_api)
        self.reply_publisher = Publisher(self.configuration, self.websocket)
        self.publishers.append(self.reply_publisher)

        def on_message(_websocket: WebSocket.WebSocketApp, message: str) -> None:
            self.stream.on_next(message)

        def on_open(_websocket: WebSocket.WebSocketApp) -> None:
            callback(SUCCESS, self)

        def on_error(_websocket: WebSocket.WebSocketApp, error: str) -> None:
            callback(error, None)

        def on_close(_websocket: WebSocket.WebSocketApp) -> None:
            print('### session %s closed ###' % server_url)

        self.websocket.on_message = on_message
        self.websocket.on_open = on_open
        self.websocket.on_error = on_error
        self.websocket.on_close = on_close

        self.websocket.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})

    def create_publisher(self) -> Publisher:
        configuration = APIConfiguration(self.xc_api)
        publisher = Publisher(configuration, self.websocket)
        self.publishers.append(publisher)
        return publisher

    def create_subscriber(self) -> Subscriber:
        configuration = APIConfiguration(self.xc_api)
        subscriber = Subscriber(configuration, self.websocket, self.stream, self.reply_publisher)
        self.subscribers.append(subscriber)
        return subscriber

    def dispose_subscriber(self, subscriber: Subscriber) -> None:
        remove_element(self.subscribers, subscriber)

    def dispose_publisher(self, publisher: Publisher) -> None:
        remove_element(self.publishers, publisher)

    def dispose_publishers_subscribers(self) -> None:
        for publisher in self.publishers:
            self.dispose_publisher(publisher) 
        for subscriber in self.subscribers:
            self.dispose_subscriber(subscriber) 
        self.publishers = []
        self.subscribers = []

    def close_session(self) -> None:
        self.dispose_publishers_subscribers()
        self.websocket.close()
