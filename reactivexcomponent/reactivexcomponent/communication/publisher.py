import json
from reactivexcomponent.configuration.serializer import to_websocket_input_format
from reactivexcomponent.configuration.api_configuration import format_fsharp_field


class Publisher:

    def __init__(self, apiconfiguration, websocket_instance):
        self.configuration = apiconfiguration
        self.websocket = websocket_instance

    def _get_header_config(self, component_code, state_machine_code, message_type):
        return {"StateMachineCode": format_fsharp_field(state_machine_code),
                "ComponentCode": format_fsharp_field(component_code),
                "EventCode": self.configuration.get_publisher_details(component_code,
                                                                      state_machine_code,
                                                                      message_type)["eventCode"],
                "IncomingType": 0,
                "MessageType": format_fsharp_field(message_type)}

    def _get_routing_key(self, component_code, state_machine_code, message_type):
        publisher_details = self.configuration.get_publisher_details(
            component_code, state_machine_code, message_type)
        return publisher_details['routingKey']

    def _get_data_to_send(self, component_name, state_machine_name, message_type, json_message):
        component_code = self.configuration.get_component_code(component_name)
        state_machine_code = self.configuration.get_state_machine_code(
            component_name, state_machine_name)
        header_config = self._get_header_config(component_code, state_machine_code, message_type)
        routing_key = self._get_routing_key(component_code, state_machine_code, message_type)
        return {
            "RoutingKey": routing_key,
            "ComponentCode": component_code,
            "Event": {"Header": header_config, "JsonMessage": json.dumps(json_message)}
        }

    def send_message(self, component_name, state_machine_name, message_type, json_message):
        data = self._get_data_to_send(
            component_name, state_machine_name, message_type, json_message)
        self.websocket.send(to_websocket_input_format(data))
