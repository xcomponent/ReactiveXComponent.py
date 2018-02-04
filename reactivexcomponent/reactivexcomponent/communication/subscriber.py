import json
from reactivexcomponent.configuration.websocket_bridge_configuration import EventType, Command, WebsocketTopicKind
from reactivexcomponent.configuration.serializer import command_data_websocket_format, get_header_with_incoming_type
from reactivexcomponent.configuration.serializer import deserialize, get_json_data


def get_data_to_send(topic, kind):
    return {"Header": get_header_with_incoming_type(),
            "JsonMessage": json.dumps({
                "Topic": {"Key": topic, "Kind": kind}
            })
           }

def is_same_state_machine(json_data, state_machine_code):
    same_state_machine = (json_data["stateMachineRef"]["StateMachineCode"] == state_machine_code)
    return same_state_machine

def is_same_component(json_data, component_code):
    same_component = (json_data["stateMachineRef"]["ComponentCode"] == component_code)
    return same_component

def is_subscribed(subscribed_state_machines, component_name, state_machine_name):
    subscribed = (component_name in subscribed_state_machines) and (
        state_machine_name in subscribed_state_machines[component_name])
    return subscribed


class Subscriber:

    def __init__(self, apiconfiguration, websocket_instance, subject, reply_publisher):
        self.configuration = apiconfiguration
        self.websocket = websocket_instance
        self.subscribed_state_machines = {}
        self.subject = subject
        self.observable_subscribers = []
        self.reply_publisher = reply_publisher

    # pylint: disable=unnecessary-lambda
    def _json_data_from_event(self, data):
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
            "send": lambda state_machine_ref, message_type, json_message: 
                    self_subscriber.reply_publisher.\
                    send_with_state_machine_ref(state_machine_ref, message_type, json_message)
        }
        return {
            "stateMachineRef": state_machine_ref,
            "jsonMessage": json.loads(json_data["JsonMessage"])
        }

    def _prepare_state_machine_updates(self, component_name, state_machine_name):
        component_code = self.configuration.get_component_code(component_name)
        state_machine_code = self.configuration.get_state_machine_code(
            component_name, state_machine_name)
        filtered_observable = self.subject.map(lambda raw_message: deserialize(raw_message)) \
                                 .filter(lambda data: data["command"] == Command.update) \
                                 .map(lambda data: self._json_data_from_event(data["stringData"])) \
                                 .filter(lambda json_data: is_same_component(json_data, component_code) and 
                                         is_same_state_machine(json_data, state_machine_code))
        return filtered_observable

    def _add_subscribe_state_machine(self, component_name, state_machine_name):
        self.subscribed_state_machines[component_name] = (
            self.subscribed_state_machines).get(component_name, [])
        (self.subscribed_state_machines[component_name]).append(
            state_machine_name)

    def _send_subscribe_request_to_topic(self, topic, kind):
        data = get_data_to_send(topic, kind)
        command_data = {"Command": Command.subscribe, "Data": data}
        input_data = command_data_websocket_format(command_data)
        self.websocket.send(input_data)

    def _send_subscribe_request(self, component_name, state_machine_name):
        component_code = self.configuration.get_component_code(component_name)
        state_machine_code = self.configuration.get_state_machine_code(
            component_name, state_machine_name)
        topic = self.configuration.get_subscriber_topic(
            component_code, state_machine_code, EventType.Update)
        self._send_subscribe_request_to_topic(topic, WebsocketTopicKind.Public)
        self._add_subscribe_state_machine(component_name, state_machine_name)

    def can_subscribe(self, component_name, state_machine_name):
        component_code = self.configuration.get_component_code(component_name)
        state_machine_code = self.configuration.get_state_machine_code(component_name, state_machine_name)
        return self.configuration.contains_subscriber(component_code, state_machine_code, EventType.Update)

    def get_state_machine_updates(self, component_name, state_machine_name):
        filtered_observable = self._prepare_state_machine_updates(component_name, state_machine_name)
        self._send_subscribe_request(component_name, state_machine_name)
        return filtered_observable

    # pylint: disable=redefined-outer-name
    def subscribe(self, component_name, state_machine_name, state_machine_update_listener):
        observable_subscriber = self._prepare_state_machine_updates(component_name, state_machine_name).subscribe(
            lambda json_data: state_machine_update_listener(json_data))
        self.observable_subscribers.append(observable_subscriber)
        self._send_subscribe_request(component_name, state_machine_name)
    # pylint: enable=unnecessary-lambda, redefined-outer-name

    def dispose_observable_subscribers(self):
        for i in range(len(self.observable_subscribers)):
            self.observable_subscribers[i].dispose()
        self.observable_subscribers = []

    # pylint: disable=invalid-name
    def remove_subscribed_state_machines(self, component_name, state_machine_name):
        index = self.subscribed_state_machines[component_name].index(state_machine_name)
        del self.subscribed_state_machines[component_name][index]
    # pylint: enable=invalid-name

    def unsubscribe(self, component_name, state_machine_name):
        if is_subscribed(self.subscribed_state_machines, component_name, state_machine_name):
            component_code = self.configuration.get_component_code(component_name)
            state_machine_code = self.configuration.get_state_machine_code(component_name, state_machine_name)
            topic = self.configuration.get_subscriber_topic(component_code, state_machine_code, EventType.Update)
            kind = WebsocketTopicKind.Public
            data = get_data_to_send(topic, kind)
            command_data = {
                "Command": Command.unsubscribe,
                "Data": data
            }
            self.websocket.send(command_data_websocket_format(command_data))
            self.remove_subscribed_state_machines(component_name, state_machine_name)

    def subscribe(self, component_name, state_machine_name):
        self._send_subscribe_request(component_name, state_machine_name)
