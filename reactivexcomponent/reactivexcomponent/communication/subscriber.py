import json
from rx import Observable
from reactivexcomponent.communication.publisher import Publisher
from reactivexcomponent.configuration.websocket_bridge_configuration import EventType
from reactivexcomponent.configuration.websocket_bridge_configuration import WebsocketTopicKind
from reactivexcomponent.configuration.websocket_bridge_configuration import Command
from reactivexcomponent.configuration.serializer import command_data_websocket_format
from reactivexcomponent.configuration.serializer import get_header_with_incoming_type
from reactivexcomponent.configuration.serializer import deserialize
from reactivexcomponent.configuration.serializer import get_json_data


def get_data_to_send(topic, kind):
    return {"Header": get_header_with_incoming_type(),
            "JsonMessage": json.dumps({
                "Topic": {"Key": topic, "Kind": kind}
            })
           }

# pylint: disable=unused-argument


def state_machine_update_listener(data):
    pass
# pylint: enable=unused-argument


def is_same_state_machine(json_data, state_machine_code):
    same_state_machine = (json_data["stateMachineRef"]["StateMachineCode"] == state_machine_code)
    return same_state_machine

def is_same_component(json_data, component_code):
    same_component = (json_data["stateMachineRef"]["ComponentCode"] == component_code)
    return same_component


class Subscriber:

    reply_publisher = Publisher

    def __init__(self, apiconfiguration, websocket_instance, reply_publisher):
        self.configuration = apiconfiguration
        self.websocket = websocket_instance
        self.subscribed_state_machines = {}
        self.observable_msg = Observable.from_(self.websocket, "message")
        self.reply_publisher = reply_publisher

    def json_data_from_event(self, data, topic):
        json_data = get_json_data(data)
        component_code = json_data["Header"]["ComponentCode"]["Fields"][0]
        state_machine_code = json_data["Header"]["StateMachineCode"]["Fields"][0]
        state_code = json_data["Header"]["StateCode"]["Fields"][0]
        self_subscriber = self
        state_machine_ref = {
            "StateMachineId": json_data["Header"]["StateMachineId"]["Fields"][0],
            "AgentId": json_data["Header"]["AgentId"]["Fields"][0],
            "StateMachineCode": json_data["Header"]["StateMachineCode"]["Fields"][0],
            "ComponentCode": json_data["Header"]["ComponentCode"]["Fields"][0],
            "StateName": self_subscriber.configuration.get_state_name(component_code, state_machine_code, state_code),
            "send": lambda (state_machine_ref, message_type, json_message): self_subscriber.reply_publisher.send_with_state_machine_ref(state_machine_ref, message_type, json_message)
        }
        return {
            "stateMachineRef": state_machine_ref,
            "jsonMessage": json.loads(json_data["JsonMessage"])
        }

    def _prepare_state_machine_updates(self, component_name, state_machine_name):
        component_code = self.configuration.get_component_code(component_name)
        state_machine_code = self.configuration.get_state_machine_code(
            component_name, state_machine_name)
        filtered_observable = self.observable_msg.map(lambda raw_message: deserialize(raw_message.data)) \
                                 .filter(lambda data: data["command"] == Command.update) \
                                 .map(lambda data: json_data_from_event(data["stringData"], data["topic"])) \
                                 .filter(lambda json_data: is_same_component(json_data, component_code) and 
                                         is_same_state_machine(json_data, state_machine_code))
        return filtered_observable

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

    def subscriber(self, component_name, state_machine_name, state_machine_update_listener):
        observable_subscriber = self._prepare_state_machine_updates(component_name, state_machine_name).subscribe(
            lambda json_data: state_machine_update_listener(json_data))
        self.send_subscribe_request(component_name, state_machine_name)
