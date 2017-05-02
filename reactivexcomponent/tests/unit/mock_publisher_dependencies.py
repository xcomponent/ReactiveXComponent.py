import json
import lxml
from unittest.mock import MagicMock

COMPONENT_CODE = -725052640
STATE_MACHINE_CODE = -2027871621
EVENT_CODE = 8
MESSAGE_TYPE = "XComponent.Devinette.UserObject.CheckWord"
ROUTING_KEY = "input.1_0.microservice1.Devinette.DevinetteChecker"
GUI_EXAMPLE = "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx"
SESSION_DATA = "sessionData"

guid = MagicMock(["create"], key = "guid")
guid.create = MagicMock(return_value = GUI_EXAMPLE)
guid.create("create", key = "guid")
guid.create.assert_called_with("create", key="guid")


def get_header():
    header = {
        "StateMachineCode": {"Case": "Some", "Fields": [STATE_MACHINE_CODE]},
        "ComponentCode": {"Case": "Some", "Fields": [COMPONENT_CODE]},
        "EventCode": EVENT_CODE,
        "IncomingType": 0,
        "MessageType": {"Case": "Some", "Fields": [MESSAGE_TYPE]}
    }
    return header


json_message = {"Name": "My Name"}


def get_correct_data():
    return {
        "event": {
            "Header": get_header(),
            "JsonMessage": json.dumps(json_message)
        },
        "routingKey": ROUTING_KEY
    }


def get_correct_websocket_input_format():
    correct_data = get_correct_data()
    correct_websocket_input_format = correct_data["routingKey"] + " " + str(
        correct_data["event"]["Header"]["ComponentCode"]["Fields"][0]) + " " + json.dumps(correct_data["event"])
    return correct_websocket_input_format


# Mocking configuration

Publisher = MagicMock(["get_component_code", "get_state_machine_code",
                       "get_publisher_details", "sender" ], key="publisher")


#root = MagicMock()

def side_effect_1(component_name):
    if component_name is None:
        raise Exception("Error")
    return COMPONENT_CODE


Publisher.get_component_code = MagicMock(side_effect = side_effect_1)
# publisher.get_component_code("component_name")
# publisher.get_component_code(None)


def side_effect_2(component_name, state_machine_name):
    if (component_name is None) or (state_machine_name is None):
        raise Exception("Error")
    return STATE_MACHINE_CODE


Publisher.get_state_machine_code = MagicMock(side_effect = side_effect_2)
# publisher.get_state_machine_code("component_name","state_machine_name")
# publisher.get_state_machine_code("component_name",None)


def side_effect_3(component_code, state_machine_code, message_type):
    return {
        "eventCode": EVENT_CODE,
        "routingKey": ROUTING_KEY
    }


Publisher.get_publisher_details = MagicMock(side_effect = side_effect_3)

# Mocking websocket


def create_mock_websocket():
    websocket = MagicMock(["send"], "websocket")
    return websocket


class ReturnMock:
    
    Mock = {
        "Publisher": Publisher,
        "create_mock_websocket": create_mock_websocket(),
        "json_message": json_message,
        "message_type": MESSAGE_TYPE,
        "correct_data": get_correct_data(),
        "get_correct_websocket_input_format": get_correct_websocket_input_format(),
        "gui_example": GUI_EXAMPLE
    }
