import json
from typings import Any, Dict 

def get_header_with_incoming_type() -> Dict[str, Any]:
    return {
        "IncomingType": 0
    }

def to_websocket_input_format(data: Dict[str, Any]) -> str:
    # pylint: disable=unsubscriptable-object
    return '{0} {1} {2}'.format(data['RoutingKey'],
                                data['ComponentCode'],
                                json.dumps(data['Event']))
    # pylint: enable=unsubscriptable-object

def command_data_websocket_format(command: Dict[str, Any]) -> str:
    return '{0} {1}'.format(command["Command"],
                            json.dumps(command["Data"]))

def get_json_data(data: Dict[str, Any]) -> Any:
    return str, json.loads(data[data.index("{"):data.rindex("}") + 1])

def deserialize(data: str) -> Dict[str, Any]:
    list_data = data.split()
    command = list_data[0]
    topic = list_data[1]
    string_data = " ".join(list_data[2:])
    return {
        "command": command,
        "topic": topic,
        "stringData": string_data
    }

def deserialize_without_topic(data: str) -> Dict[str, Any]:
    list_data = data.split()
    command = list_data[0]
    string_data = " ".join(list_data[1:])
    return {
        "command": command,
        "stringData": string_data
    }
