from lxml import etree
from reactivexcomponent.configuration.websocket_bridge_configuration import EventType

NAMESPACE = {'xmlns': 'http://xcomponent.com/DeploymentConfig.xsd'}


def format_fsharp_field(value):
    return {"Case": "Some", "Fields": [value]}


def find_state_machine_by_name(component, state_machine_name):
    state_machine = None
    for state_machines in component.findall('xmlns:stateMachines', NAMESPACE):
        for state_mach in state_machines.findall('xmlns:stateMachine', NAMESPACE):
            if state_mach.attrib['name'] == state_machine_name:
                state_machine = state_mach
    if state_machine is None:
        raise Exception('State Machine %s not found' % state_machine_name)
    return state_machine


def find_state_machine_by_code(component, state_machine_code):
    state_machine = None
    for state_machines in component.findall('xmlns:stateMachines', NAMESPACE):
        for state_mach in state_machines.findall('xmlns:stateMachine', NAMESPACE):
            if int(state_mach.attrib['id']) == state_machine_code:
                state_machine = state_mach
    if state_machine is None:
        raise Exception('State Machine %s not found' % state_machine_code)
    return state_machine


def find_state_by_code(state_machine, state_code):
    state = None
    for stat in state_machine.findall('xmlns:states', NAMESPACE)[0].\
            findall('xmlns:State', NAMESPACE):
        if int(stat.attrib["id"]) == state_code:
            state = stat
    if state is None:
        raise Exception('State %s not found' % state_code)
    return state


class APIConfiguration:

    def __init__(self, file):
        # pylint: disable=no-member
        tree = etree.parse(file)
        data = etree.tostring(tree)
        self.root = etree.fromstring(data)
        # pylint: enable=no-member

    def _find_component(self, component_name):
        for component in ((self.root).findall('xmlns:codesConverter', NAMESPACE))[0].\
                findall('xmlns:components', NAMESPACE)[0].\
                findall('xmlns:component', NAMESPACE):
            if component.attrib['name'] == component_name:
                return component

    def _find_component_by_name(self, component_name):
        component = self._find_component(component_name)
        if component is None:
            raise Exception('Component %s not found' % component_name)
        return component

    def _find_component_name(self, component_code):
        for component in ((self.root).findall('xmlns:codesConverter', NAMESPACE))[0].\
                findall('xmlns:components', NAMESPACE)[0].\
                findall('xmlns:component', NAMESPACE):
            if int(component.attrib['id']) == component_code:
                return component

    def _find_component_by_code(self, component_code):
        component = self._find_component_name(component_code)
        if component is None:
            raise Exception('Component %s not found' % component_code)
        return component

    def get_component_code(self, component_name):
        component = self._find_component_by_name(component_name)
        return int(component.attrib['id'])

    def get_state_machine_code(self, component_name, state_machine_name):
        component = self._find_component_by_name(component_name)
        state_machine = find_state_machine_by_name(component, state_machine_name)
        return int(state_machine.attrib['id'])

    def contains_publisher(self, component_code, state_machine_code, message_type):
        return self._get_publisher(component_code, state_machine_code, message_type) != None

    def contains_state_machine(self, component_name, state_machine_name):
        component = self._find_component(component_name)
        contain = False
        if component is not None:
            for state_mach in component.findall('xmlns:stateMachines', NAMESPACE)[0].\
                                        findall('xmlns:stateMachine', NAMESPACE):
                if state_mach.attrib['name'] == state_machine_name:
                    contain = True
        return contain

    def contains_subscriber(self, component_code, state_machine_code, event_type):
        return self._get_subscriber(component_code, state_machine_code, event_type) != None

    def _get_publisher(self, component_code, state_machine_code, message_type):
        publisher = None
        for publish in ((self.root).findall('xmlns:clientAPICommunication', NAMESPACE))[0] \
                .findall('xmlns:publish', NAMESPACE):
            if (int(publish.attrib['componentCode']) == component_code) \
                and (int(publish.attrib['stateMachineCode']) == state_machine_code) \
                    and (publish.attrib['event'] == message_type):
                publisher = publish
        return publisher

    def get_publisher_details(self, component_code, state_machine_code, message_type):
        publisher = self._get_publisher(component_code, state_machine_code, message_type)
        if publisher is None:
            message = 'publisher not found - component code : ' \
                ' %i - statemachine code : %i - message type : %s'
            raise Exception(message % (component_code, state_machine_code, message_type))
        return {
            'eventCode': int(publisher.attrib['eventCode']),
            'routingKey': publisher.findall('xmlns:topic', NAMESPACE)[0].text
        }

    # pylint: disable=unused-argument
    def _get_subscriber(self, component_code, state_machine_code, event_type):
        subscriber = None
        for subscrib in ((self.root).findall('xmlns:clientAPICommunication', NAMESPACE))[0].\
                findall('xmlns:subscribe', NAMESPACE):
            if subscrib.attrib['eventType'] == EventType.Update:
                if (int(subscrib.attrib['componentCode']) == component_code) \
                        and (int(subscrib.attrib['stateMachineCode']) == state_machine_code):
                    subscriber = subscrib
        return subscriber
    # pylint: enable=unused-argument

    def get_subscriber_topic(self, component_code, state_machine_code, event_type):
        subscriber = self._get_subscriber(component_code, state_machine_code, event_type)
        if subscriber is None:
            raise Exception('Subscriber not found - component code: %i - statemachine code: %i' %
                            (component_code, state_machine_code))
        return subscriber.findall('xmlns:topic', NAMESPACE)[0].text

    def get_state_name(self, component_code, state_machine_code, state_code):
        component = self._find_component_by_code(component_code)
        state_machine = find_state_machine_by_code(component, state_machine_code)
        state = find_state_by_code(state_machine, state_code)
        return state.attrib["name"]
