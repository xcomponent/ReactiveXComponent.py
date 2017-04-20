import websocket
from reactivexcomponent.configuration.serializer import *
import json
import ssl
from lxml import etree
            
class publisher:
	
	def getXmlContent(self):
		tree=etree.parse(self.file)
		tree1=etree.tostring(tree)
		rt=etree.fromstring(tree1)
		n={'xmlns':'http://xcomponent.com/DeploymentConfig.xsd'}
		self.root=rt
		self.ns=n
	
	def findComponent(self,componentName):
		for component in ((self.root).findall('xmlns:codesConverter',self.ns))[0].findall('xmlns:components',self.ns)[0].findall('xmlns:component',self.ns):
			if (component.attrib['name']==componentName):
				return component
	
	def findComponentByName(self, componentName):
		component=self.findComponent(componentName)
		if (component==[]):
			raise Exception('Component %s not found' % componentName)
		return component			
	
	def getComponentCode(self,componentName):
		component=self.findComponentByName(componentName)
		return int(component.attrib['id'])
		
	def findStateMachineByName(self,component,stateMachineName):
		stateMachine=[]
		for stateMachines in component.findall('xmlns:stateMachines',self.ns):
			for stateMach in stateMachines.findall('xmlns:stateMachine',self.ns):
				if (stateMach.attrib['name']==stateMachineName):
					stateMachine=stateMach
		if (stateMachine==[]):
			raise Exception('State Machine %s not found' % StateMachineName)
		return stateMachine
		
	def getStateMachineCode(self,componentName,stateMachineName):
		component=self.findComponentByName(componentName)
		stateMachine=self.findStateMachineByName(component,stateMachineName)
		return int(stateMachine.attrib['id'])

	def getPublisher(self,componentCode,stateMachineCode,messageType):
		for publish in ((self.root).findall('xmlns:clientAPICommunication',self.ns))[0].findall('xmlns:publish',self.ns):
			if ((int(publish.attrib['componentCode'])==componentCode) and (int(publish.attrib['stateMachineCode'])==stateMachineCode) and (publish.attrib['event']==messageType)):
				return publish

	def getPublisherDetails(self,componentCode,stateMachineCode,messageType):
		publish=self.getPublisher(componentCode,stateMachineCode,messageType)
		if (publish=={}):
			raise Exception('publisher not found - component code : %i - statemachine code : %i - message type : %s' % (componentCode,stateMachineCode,messageType))
		return {'eventCode':int(publish.attrib['eventCode']),'routingKey':publish.findall('xmlns:topic',self.ns)[0].text}
		
	def getSubscriber(self,componentCode,stateMachineCode,eventType):
		for subscribe in ((self.root).findall('xmlns:clientAPICommunication',self.ns))[0].findall('xmlns:subscribe',self.ns):
			if ((int(subscribe.attrib['componentCode'])==componentCode) and (int(subscribe.attrib['stateMachineCode'])==stateMachineCode) and ((subscribe.attrib['eventType']).upper==eventType)):
				return subscribe
	
	def getSubscriberTopic(self,componentCode,stateMachineCode,eventType):
		subscribe=self.getSubscriber(componentCode,stateMachineCode,eventType)
		if (subscriber==[]):
			raise Exception('Subscriber not found - component code: %i - statemachine code: %i' % (componentCode,stateMachineCode))
		return subscribe.findall('xmlns:topic',self.ns)[0].text
    
	def getFSharpFormat(self,value):
		return {"Case":"Some", "Fields":[value]}

	def getHeaderConfig(self,componentCode,stateMachineCode,messageType):
		return {"StateMachineCode":self.getFSharpFormat(stateMachineCode),
				"ComponentCode":self.getFSharpFormat(componentCode),
				"EventCode":self.getPublisherDetails(componentCode,stateMachineCode,messageType)["eventCode"],
				"IncomingType":0,
				"MessageType":self.getFSharpFormat(messageType)}
    
	def getRoutingKey(self,componentCode,stateMachineCode,messageType):
		publish=self.getPublisherDetails(componentCode,stateMachineCode,messageType)
		return publish['routingKey']
	
	def getDataToSend(self,componentName,stateMachineName,messageType,jsonMessage):
		componentCode=self.getComponentCode(componentName)
		stateMachineCode=self.getStateMachineCode(componentName,stateMachineName)
		headerConfig=self.getHeaderConfig(componentCode,stateMachineCode,messageType)
		routingKey=self.getRoutingKey(componentCode,stateMachineCode,messageType)
		return {"RoutingKey":routingKey,"ComponentCode":componentCode, "Event":{"Header":headerConfig,"JsonMessage":json.dumps(jsonMessage)}}


	def sender(self,componentName,stateMachineName,messageType,jsonMessage):
		data=self.getDataToSend(componentName,stateMachineName,messageType,jsonMessage)
		self.webSocketInput=serializer.convertToWebsocketInputFormat(data)
		self.websocket.send(self.webSocketInput)
