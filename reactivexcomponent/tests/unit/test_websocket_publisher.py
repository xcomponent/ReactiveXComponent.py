import unittest
from mock import Mock
from reactivexcomponent.communication.publisher import Publisher
from mock_publisher_dependencies import ReturnMock as Moc
from reactivexcomponent.configuration.serializer import to_websocket_input_format


class TestWebSocketPublisher(unittest.TestCase):

    def setUp(self):
        self.publisher = Publisher()
        self.publisher.get_component_code = Moc.Mock["Publisher"].get_component_code
        self.publisher.get_state_machine_code = Moc.Mock["Publisher"].get_state_machine_code
        self.publisher.get_publisher_details = Moc.Mock["Publisher"].get_publisher_details
        self.publisher.websocket = Moc.Mock["create_mock_websocket"]

    def test_send_method(self):
        self.publisher.websocket.send = Mock()
        self.publisher.sender("component_name", "state_machine_name",
                              Moc.Mock["message_type"], Moc.Mock["json_message"])
        self.publisher.websocket.send.assert_called_once()
        self.publisher.websocket.send.assert_called_with(
            Moc.Mock["get_correct_websocket_input_format"])


if __name__ == "__main__":
    unittest.main()
