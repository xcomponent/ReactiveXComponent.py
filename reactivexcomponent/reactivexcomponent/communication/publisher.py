import json
from reactivexcomponent.configuration.serializer import to_websocket_input_format
from reactivexcomponent.configuration.api_configuration import format_fsharp_field


class Publisher:

    def __init__(self, apiconfiguration, websocket_instance):
        self.configuration = apiconfiguration
        self.websocket = websocket_instance

    def _header_config(self, component_code, state_machine_code, message_type):
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

    def _data_to_send(self, component_name, state_machine_name, message_type, json_message):
        component_code = self.configuration.get_component_code(component_name)
        state_machine_code = self.configuration.get_state_machine_code(
            component_name, state_machine_name)
        header_config = self._header_config(component_code, state_machine_code, message_type)
        routing_key = self._get_routing_key(component_code, state_machine_code, message_type)
        return {
            "RoutingKey": routing_key,
            "ComponentCode": component_code,
            "Event": {"Header": header_config, "JsonMessage": json.dumps(json_message)}
        }

    def can_publish(self, component_name, state_machine_name, message_type):
        if self.configuration.contains_state_machine(component_name, state_machine_name):
            component_code = self.configuration.get_component_code(component_name)
            state_machine_code = self.configuration.get_state_machine_code(component_name, state_machine_name)
            return self.configuration.contains_publisher(component_code, state_machine_code, message_type)
        return False

    def send_message(self, component_name, state_machine_name, message_type, json_message):
        data = self._data_to_send(
            component_name, state_machine_name, message_type, json_message)
        self.websocket.send(to_websocket_input_format(data))
    
    def _header_config_ref(self, component_code, state_machine_code, message_type, state_machine_id, agent_id):
        return {
            "StateMachineId": format_fsharp_field(state_machine_id),
            "AgentId": format_fsharp_field(agent_id),
            "StateMachineCode": format_fsharp_field(state_machine_code),
            "ComponentCode": format_fsharp_field(component_code),
            "EventCode": self.configuration.get_publisher_details(component_code,
                                                                  state_machine_code,
                                                                  message_type)["eventCode"],
            "IncomingType": 0,
            "MessageType": format_fsharp_field(message_type)
            }

    def _data_to_send_with_state_machine_ref(self, state_machine_ref, message_type, json_message):
        component_code = state_machine_ref["ComponentCode"]
        state_machine_code = state_machine_ref["StateMachineCode"]
        header_config = self._header_config_ref(component_code, state_machine_code, message_type,
                                                state_machine_ref["StateMachineId"], state_machine_ref["AgentId"])
        routing_key = self._get_routing_key(component_code, state_machine_code, message_type)
        return {
            "RoutingKey": routing_key,
            "ComponentCode": component_code,
            "Event": {
                "Header": header_config,
                "JsonMessage": json.dumps(json_message)
            }
        }

    def send_with_state_machine_ref(self, state_machine_ref, message_type, json_message):
        data = self._data_to_send_with_state_machine_ref(state_machine_ref, message_type, json_message)
        self.websocket.send(to_websocket_input_format(data))
