import uuid
import json
from unittest.mock import MagicMock
from reactivexcomponent.configuration.websocket_bridge_configuration import WebsocketTopicKind


OUTPUT_TOPIC = "output.1_0.microservice1.Devinette.DevinetteStatus"
SNAPSHOT_TOPIC = "snapshot.1_0.microservice1.Devinette"
STATE_NAME = "stateName"
COMPONENT_CODE = -725052640
STATE_MACHINE_CODE = -2027871621
AGENT_ID = 1
STATE_MACHINE_ID = 2
JSON_MESSAGE = {"key": "value"}


configuration = MagicMock(["get_subscriber_topic", "get_component_code", "get_state_machine_code", "get_snapshot_topic", "get_state_name",
                           "contains_subscriber"], key="configuration")

configuration.get_snapshot_topic = MagicMock(return_value=SNAPSHOT_TOPIC)

configuration.get_state_name = MagicMock(return_value=STATE_NAME)

configuration.get_component_code = MagicMock(return_value=COMPONENT_CODE)

configuration.get_state_machine_code = MagicMock(return_value=STATE_MACHINE_CODE)


def create_mock_websocket():
    websocket = MagicMock(["send", "close"], key="websocket")
    return websocket


correct_data = {
    "Header": {"IncomingType": 0},
    "JsonMessage": json.dumps({"Topic": {"Key": OUTPUT_TOPIC, "kind": WebsocketTopicKind.Public}})
}


json_data = {
    "Header": {
        "StateMachineCode": {"Case": "Some", "Fields": [STATE_MACHINE_CODE]},
        "ComponentCode": {"Case": "Some", "Fields": [COMPONENT_CODE]},
        "StateMachineId": {"Case": "Some", "Fields": [STATE_MACHINE_ID]},
        "AgentId": {"Case": "Some", "Fields": [AGENT_ID]},
        "StateCode": {"Case": "Some", "Fields": [0]}
    },
    "JsonMessage": json.dumps(JSON_MESSAGE)
}

update_response = "update " + "topic " + json.dumps(json_data)

correct_received_data = {
    "stateMachineRef": {
        "StateMachineCode": json_data["Header"]["StateMachineCode"]["Fields"][0],
        "ComponentCode": json_data["Header"]["ComponentCode"]["Fields"][0],
        "AgentId": AGENT_ID,
        "StateName": STATE_NAME,
        "send": lambda JSON_MESSAGE: []
    },
    "jsonMessage": JSON_MESSAGE
}

correct_subscribe_request = "subscribe " + json.dumps(correct_data)
correct_unsubscribe_request = "unsubscribe " + json.dumps(correct_data)
