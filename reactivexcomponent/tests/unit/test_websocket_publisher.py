import unittest
from mock import Mock
from reactivexcomponent.communication.publisher import Publisher
import mock_publisher_dependencies as dependencies


class TestWebSocketPublisher(unittest.TestCase):

    def setUp(self):
        self.publisher = Publisher(dependencies.configuration, dependencies.create_mock_websocket())

    def test_send_method(self):
        self.publisher.websocket.send = Mock()
        self.publisher.sender("component_name", "state_machine_name",
                              dependencies.MESSAGE_TYPE, dependencies.JSON_MESSAGE)
        self.publisher.websocket.send.assert_called_once()
        self.publisher.websocket.send.assert_called_with(
            dependencies.get_correct_websocket_input_format(True))


if __name__ == "__main__":
    unittest.main()
