import unittest
import json
from reactivexcomponent.communication.publisher import *

p=Publisher()
p.file="data\\WebSocket_NewDevinetteApi_test.xcApi"
p.get_xml_content()

class test_publisher(unittest.TestCase):
    
    def test_get_component_code(self):
        """get_component_code should return the right code given an existing component name"""
        code=p.get_component_code('Devinette')
        correct_code=-725052640
        self.assertEqual(code,correct_code)
        """get_component_code throws exception when using an unkonwn component name"""
        component_name='New'
        with self.assertRaises(Exception):
            p.get_component_code(component_name)

    def test_get_state_machine_code(self):
        """get_state_machine_code should return the right code given existing component name and statemachine name"""
        code=p.get_state_machine_code('Devinette','Devinette')
        correct_code=-725052640
        self.assertEqual(code,correct_code)

        code=p.get_state_machine_code('Devinette','DevinetteStatus')
        correct_code=2089109814
        self.assertEqual(code,correct_code)
        """get_state_machine_code throws exception when using an unkonwn state machine name"""
        with self.assertRaises(Exception):
            p.get_state_machine_code('New')

    def test_get_publisher_details(self):
        """get_publisher_details should return the right publisher details given existing component and stateMachine codes"""
        correct_publish={'eventCode':8,'routingKey':'input.1_0.microservice1.Devinette.DevinetteChecker'}
        publish=p.get_publisher_details(-725052640,-2027871621,'XComponent.Devinette.UserObject.CheckWord')
        self.assertEqual(publish,correct_publish)
        """GetPublisherDetails should throw exeption when using an unknown stateMachine name"""
        component_code=101
        state_machine_code=102
        message_type='type'
        with self.assertRaises(Exception):
            p.get_publisher_details(component_code,state_machine_code,message_type)

if __name__=="__main__":
    unittest.main()        
        
