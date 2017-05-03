""" API Configuartion """

from lxml import etree

EVENT_TYPE = {"Update": "UPDATE", "Error": "ERROR"}

KINDS = {"Snapshot": 1, "Private": 2, "Public": 3}

COMMANDS = {"hb": "hb", "update": "update", "subscribe": "subscribe",
            "get_xc_api": "getXcApi", "get_xc_api_list": "getXcApiList", "get_model": "getModel"}

NAME_SPACE = {'xmlns': 'http://xcomponent.com/DeploymentConfig.xsd'}


def format_fsharp_field(value):
    return {"Case": "Some", "Fields": [value]}


class APIConfiguration:

    def __init__(self, file):
        self.file = file
        self.root = None

    def get_xml_content(self):
        # pylint: disable=no-member
        tree = etree.parse(self.file)
        data = etree.tostring(tree)
        root = etree.fromstring(data)
        self.root = root

    def _find_component(self, component_name):
        for component in ((self.root).findall('xmlns:codesConverter', NAME_SPACE))[0].\
                findall('xmlns:components', NAME_SPACE)[0].\
                findall('xmlns:component', NAME_SPACE):
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
        for state_machines in component.findall('xmlns:stateMachines', NAME_SPACE):
            for state_mach in state_machines.findall('xmlns:stateMachine', NAME_SPACE):
                if state_mach.attrib['name'] == state_machine_name:
                    state_machine = state_mach
        if state_machine is None:
            raise Exception('State Machine %s not found' % state_machine_name)
        return state_machine

    def get_state_machine_code(self, component_name, state_machine_name):
        component = self._find_component_by_name(component_name)
        state_machine = self._find_state_machine_by_name(component, state_machine_name)
        return int(state_machine.attrib['id'])

    def _get_publisher(self, component_code, state_machine_code, message_type):
        for publisher in ((self.root).findall('xmlns:clientAPICommunication', NAME_SPACE))[0] \
                .findall('xmlns:publish', NAME_SPACE):
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
            'routingKey': publisher.findall('xmlns:topic', NAME_SPACE)[0].text
        }

    def _get_subscriber(self, component_code, state_machine_code, event_type):
        for subscriber in ((self.root).findall('xmlns:clientAPICommunication', NAME_SPACE))[0].\
                findall('xmlns:subscribe', NAME_SPACE):
            if subscriber.attrib['eventType'] == 'UPDATE':
                if (int(subscriber.attrib['componentCode']) == component_code) and (int(subscriber.attrib['stateMachineCode']) == state_machine_code):
                    return subscriber

    def get_subscriber_topic(self, component_code, state_machine_code, event_type):
        subscriber = self._get_subscriber(component_code, state_machine_code, event_type)
        if subscriber is None:
            raise Exception('Subscriber not found - component code: %i - statemachine code: %i' %
                            (component_code, state_machine_code))
        return subscriber.findall('xmlns:topic', NAME_SPACE)[0].text
