import json
from reactivexcomponent.configuration.serializer import Serializer
from lxml import etree

class Publisher:

    def get_xml_content(self):
        tree = etree.parse(self.file)
        data = etree.tostring(tree)
        root = etree.fromstring(data)
        namespace = {'xmlns': 'http://xcomponent.com/DeploymentConfig.xsd'}
        self.root = root
        self.namespace = namespace

    def _find_component(self, component_name):
        for component in ((self.root).findall('xmlns:codesConverter', self.namespace))[0].\
                findall('xmlns:components', self.namespace)[0].\
                findall('xmlns:component', self.namespace):
            if component.attrib['name'] == component_name:
                return component

    def _find_component_by_name(self, component_name):
        component = self._find_component(component_name)
        if component is None:
            raise Exception('Component %s not found' % component_name)
        return component

    def get_component_code(self, component_name):
        component = self._find_component_by_name(component_name)
        return int(component.attrib['id'])

    def _find_state_machine_by_name(self, component, state_machine_name):
        state_machine = None
        for stateMachines in component.findall('xmlns:stateMachines', self.namespace):
            for stateMach in stateMachines.findall('xmlns:stateMachine', self.namespace):
                if stateMach.attrib['name'] == state_machine_name:
                    state_machine = stateMach
        if state_machine is None:
            raise Exception('State Machine %s not found' % state_machine_name)
        return state_machine

    def get_state_machine_code(self, component_name, state_machine_name):
        component = self._find_component_by_name(component_name)
        state_machine = self._find_state_machine_by_name(component, state_machine_name)
        return int(state_machine.attrib['id'])

    def _get_publisher(self, component_code, state_machine_code, message_type):
        for publisher in ((self.root).findall('xmlns:clientAPICommunication', self.namespace))[0] \
            .findall('xmlns:publish', self.namespace):

            if (int(publisher.attrib['componentCode']) == component_code) \
                and (int(publisher.attrib['stateMachineCode']) == state_machine_code) \
                    and (publisher.attrib['event'] == message_type):
                return publisher

    def get_publisher_details(self, component_code, state_machine_code, message_type):
        publisher = self._get_publisher(component_code, state_machine_code, message_type)
        if publisher is None:
            message = 'publisher not found - component code : ' \
                ' %i - statemachine code : %i - message type : %s'

            raise Exception(message % (component_code, state_machine_code, message_type))
        return {
            'eventCode': int(publisher.attrib['eventCode']),
            'routingKey': publisher.findall('xmlns:topic', self.namespace)[0].text
        }

    def get_subscriber(self, component_code, state_machine_code, event_type):
        for subscribe in ((self.root).findall('xmlns:clientAPICommunication', self.namespace))[0] \
            .findall('xmlns:subscribe', self.namespace):

            if (int(subscribe.attrib['componentCode']) == component_code) \
                and (int(subscribe.attrib['stateMachineCode']) == state_machine_code) \
                    and ((subscribe.attrib['eventType']).upper == event_type):
                return subscribe

    def get_subscriber_topic(self, component_code, state_machine_code, event_type):
        subscriber = self.get_subscriber(component_code, state_machine_code, event_type)
        if subscriber is None:
            raise Exception('Subscriber not found - component code: %i - statemachine code: %i' %
                            (component_code, state_machine_code))
        return subscriber.findall('xmlns:topic', self.namespace)[0].text

    def _get_fsharp_format(self, value):
        return {"Case": "Some", "Fields": [value]}

    def _get_header_config(self, component_code, state_machine_code, message_type):
        return {"StateMachineCode": self._get_fsharp_format(state_machine_code),
                "ComponentCode": self._get_fsharp_format(component_code),
                "EventCode": self.get_publisher_details(component_code,
                                                        state_machine_code,
                                                        message_type)["eventCode"],
                "IncomingType": 0,
                "MessageType": self._get_fsharp_format(message_type)}

    def _get_routing_key(self, component_code, state_machine_code, message_type):
        publisher = self.get_publisher_details(component_code, state_machine_code, message_type)
        return publisher['routingKey']

    def _get_data_to_send(self, component_name, state_machine_name, message_type, json_message):
        component_code = self.get_component_code(component_name)
        state_machine_code = self.get_state_machine_code(component_name, state_machine_name)
        header_config = self._get_header_config(component_code, state_machine_code, message_type)
        routing_key = self._get_routing_key(component_code, state_machine_code, message_type)
        return {
            "RoutingKey": routing_key,
            "ComponentCode": component_code,
            "Event": {"Header": header_config, "JsonMessage": json.dumps(json_message)}
        }

    def sender(self, component_name, state_machine_name, message_type, json_message):
        data = self._get_data_to_send(component_name,\
            state_machine_name, \
            message_type, json_message)

        self.web_socket_input = Serializer.convert_to_websocket_input_format(data)
        self.websocket.send(self.web_socket_input)
