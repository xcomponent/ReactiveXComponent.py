import json

class Serializer:
    def convert_to_websocket_input_format(data):
        # pylint: disable=unsubscriptable-object
        return '{0} {1} {2}'.format(data['RoutingKey'], \
            data['ComponentCode'], \
            json.dumps(data['Event']))
