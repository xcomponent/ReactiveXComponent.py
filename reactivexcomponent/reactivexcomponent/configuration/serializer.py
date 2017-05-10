import json


def get_header_with_incoming_type():
    return {
        "IncomingType": 0
    }


def to_websocket_input_format(data):
    # pylint: disable=unsubscriptable-object
    return '{0} {1} {2}'.format(data['RoutingKey'],
                                data['ComponentCode'],
                                json.dumps(data['Event']))
    # pylint: enable=unsubscriptable-object


def command_data_websocket_format(command):
    return '{0} {1}'.format(command["Command"],
                            json.dumps(command["Data"]))
