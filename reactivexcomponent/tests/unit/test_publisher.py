import unittest
import json
from reactivexcomponent.communication.publisher import *

p=publisher()
p.file="data\\WebSocket_NewDevinetteApi_test.xcApi"
p.getXmlContent()

class testPublisher(unittest.TestCase):
    
    def testgetComponentCode(self):
        """getComponentCode should return the right code given an existing component name"""
        code=p.getComponentCode('Devinette')
        correctCode=-725052640
        self.assertEqual(code,correctCode)
        """GetComponentCode throws exception when using an unkonwn component name"""
        componentName='New'
        with self.assertRaises(Exception):
            p.getComponentCode(componentName)

    def testgetStateMachineCode(self):
        """GetStateMachineCode should return the right code given existing component name and statemachine name"""
        code=p.getStateMachineCode('Devinette','Devinette')
        correctCode=-725052640
        self.assertEqual(code,correctCode)

        code=p.getStateMachineCode('Devinette','DevinetteStatus')
        correctCode=2089109814
        self.assertEqual(code,correctCode)
        """GetStateMachineCode throws exception when using an unkonwn state machine name"""
        with self.assertRaises(Exception):
            p.getStateMachineCode('New')

    def testgetPublisherDetails(self):
        """GetPublisherDetails should return the right publisher details given existing component and stateMachine codes"""
        correctPublish={'eventCode':8,'routingKey':'input.1_0.microservice1.Devinette.DevinetteChecker'}
        publish=p.getPublisherDetails(-725052640,-2027871621,'XComponent.Devinette.UserObject.CheckWord')
        self.assertEqual(publish,correctPublish)
        """GetPublisherDetails should throw exeption when using an unknown stateMachine name"""
        componentCode=101
        stateMachineCode=102
        messageType='type'
        with self.assertRaises(Exception):
            p.getPublisherDetails(componentCode,stateMachineCode,messageType)

if __name__=="__main__":
    unittest.main()        
        
