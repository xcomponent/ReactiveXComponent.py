import json


class Serializer:
    def convert_to_websocket_input_format(data):
        winput = '{0} {1} {2}'.format(
            data['RoutingKey'], data['ComponentCode'], json.dumps(data['Event']))
        return winput
