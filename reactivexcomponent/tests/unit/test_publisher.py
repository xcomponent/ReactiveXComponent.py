import unittest
import json
from reactivexcomponent.communication.publisher import Publisher


class TestPublisher(unittest.TestCase):

    def setUp(self):
        self.p = Publisher()
        self.p.file = "tests\\unit\\data\\WebSocket_NewDevinetteApi_test.xcApi"
        self.p.get_xml_content()

    def test_get_component_code(self):
        """get_component_code should return the right code given an existing component name"""
        code = self.p.get_component_code('Devinette')
        correct_code = -725052640
        self.assertEqual(code, correct_code)
        """get_component_code throws exception when using an unkonwn component name"""
        with self.assertRaises(Exception):
            self.p.get_component_code('UnkonwnComponent')

    def test_get_state_machine_code(self):
        """get_state_machine_code should return the right code given existing component name and statemachine name"""
        code = self.p.get_state_machine_code('Devinette', 'Devinette')
        correct_code = -725052640
        self.assertEqual(code, correct_code)

        code = self.p.get_state_machine_code('Devinette', 'DevinetteStatus')
        correct_code = 2089109814
        self.assertEqual(code, correct_code)
        """get_state_machine_code throws exception when using an unkonwn state machine name"""
        with self.assertRaises(Exception):
            self.p.get_state_machine_code('Devinette','UnkownStateMachine')

    def test_get_publisher_details(self):
        """get_publisher_details should return the right publisher details given existing component and stateMachine codes"""
        correct_publish = {
            'eventCode': 8, 'routingKey': 'input.1_0.microservice1.Devinette.DevinetteChecker'}
        publish = self.p.get_publisher_details(
            -725052640, -2027871621, 'XComponent.Devinette.UserObject.CheckWord')
        self.assertEqual(publish, correct_publish)
        """get_publisher_details should throw exeption when using an unknown stateMachine name"""
        component_code = 101
        state_machine_code = 102
        message_type = 'type'
        with self.assertRaises(Exception):
            self.p.get_publisher_details(
                component_code, state_machine_code, message_type)


if __name__ == "__main__":
    unittest.main()
