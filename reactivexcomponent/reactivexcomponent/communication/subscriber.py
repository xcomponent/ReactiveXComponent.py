import json
from reactivexcomponent.configuration.websocket_bridge_configuration import EventType
from reactivexcomponent.configuration.websocket_bridge_configuration import WebsocketTopicKind
from reactivexcomponent.configuration.websocket_bridge_configuration import Command
from reactivexcomponent.configuration.serializer import command_data_websocket_format
from reactivexcomponent.configuration.serializer import get_header_with_incoming_type


def get_data_to_send(topic, kind):
    return {"Header": get_header_with_incoming_type(),
            "JsonMessage": json.dumps({
                "Topic": {"Key": topic, "Kind": kind}
            })
           }


class Subscriber:

    def __init__(self, apiconfiguration, websocket_instance):
        self.configuration = apiconfiguration
        self.websocket = websocket_instance
        self.subscribed_state_machines = {}

    def add_subscribe_state_machine(self, component_name, state_machine_name):
        self.subscribed_state_machines[component_name] = (
            self.subscribed_state_machines).get(component_name, [])
        (self.subscribed_state_machines[component_name]).append(state_machine_name)

    def send_subscribe_request_to_topic(self, topic, kind):
        data = get_data_to_send(topic, kind)
        command_data = {"Command": Command.subscribe, "Data": data}
        input_data = command_data_websocket_format(command_data)
        self.websocket.send(input_data)

    def send_subscribe_request(self, component_name, state_machine_name):
        component_code = self.configuration.get_component_code(component_name)
        state_machine_code = self.configuration.get_state_machine_code(
            component_name, state_machine_name)
        topic = self.configuration.get_subscriber_topic(
            component_code, state_machine_code, EventType.Update)
        self.send_subscribe_request_to_topic(topic, WebsocketTopicKind.Public)
        self.add_subscribe_state_machine(component_name, state_machine_name)

    def subscriber(self, component_name, state_machine_name):
        self.send_subscribe_request(component_name, state_machine_name)
