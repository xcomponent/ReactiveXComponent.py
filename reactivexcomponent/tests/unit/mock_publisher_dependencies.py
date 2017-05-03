import json
from unittest.mock import MagicMock

COMPONENT_CODE = -725052640
STATE_MACHINE_CODE = -2027871621
EVENT_CODE = 8
MESSAGE_TYPE = "XComponent.Devinette.UserObject.CheckWord"
ROUTING_KEY = "input.1_0.microservice1.Devinette.DevinetteChecker"
GUI_EXAMPLE = "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx"
SESSION_DATA = "sessionData"
JSON_MESSAGE = {"Name": "My Name"}

guid = MagicMock(["create"], key="guid")
guid.create = MagicMock(return_value=GUI_EXAMPLE)
guid.create("create", key="guid")
guid.create.assert_called_with("create", key="guid")


def get_header(visibility):
    header = {
        "StateMachineCode": {"Case": "Some", "Fields": [STATE_MACHINE_CODE]},
        "ComponentCode": {"Case": "Some", "Fields": [COMPONENT_CODE]},
        "EventCode": EVENT_CODE,
        "IncomingType": 0,
        "MessageType": {"Case": "Some", "Fields": [MESSAGE_TYPE]}
    }
    return header


def get_correct_data(visibility):
    return {
        "event": {
            "Header": get_header(True),
            "JsonMessage": json.dumps(JSON_MESSAGE)
        },
        "routingKey": ROUTING_KEY
    }


def get_correct_websocket_input_format(visibility):
    correct_data = get_correct_data(True)
    correct_websocket_input_format = correct_data["routingKey"] + " " + str(
        correct_data["event"]["Header"]["ComponentCode"]["Fields"][0]) + " " + json.dumps(correct_data["event"])
    return correct_websocket_input_format

# Mocking configuration


configuration = MagicMock(["get_component_code", "get_state_machine_code",
                           "get_publisher_details"], key="configuration")


def component_code(component_name):
    if component_name is None:
        raise Exception("Error")
    return COMPONENT_CODE


configuration.get_component_code = MagicMock(side_effect=component_code)


def state_machine_code(component_name, state_machine_name):
    if (component_name is None) or (state_machine_name is None):
        raise Exception("Error")
    return STATE_MACHINE_CODE


configuration.get_state_machine_code = MagicMock(side_effect=state_machine_code)


def publisher_details(component_code, state_machine_code, message_type):
    return {
        "eventCode": EVENT_CODE,
        "routingKey": ROUTING_KEY
    }


configuration.get_publisher_details = MagicMock(side_effect=publisher_details)

# Mocking websocket


def create_mock_websocket():
    websocket = MagicMock(["send"], key="websocket")
    return websocket
