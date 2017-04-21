""" Publisher """

import json
import websocket
from reactivexcomponent.configuration.serializer import *
from lxml import etree

class Publisher:
	
	def get_xml_content(self):
		tree=etree.parse(self.file)
		tree1=etree.tostring(tree)
		rt=etree.fromstring(tree1)
		n={'xmlns':'http://xcomponent.com/DeploymentConfig.xsd'}
		self.root=rt
		self.ns=n

	def find_component(self,component_name):
		for component in ((self.root).findall('xmlns:codesConverter',self.ns))[0].findall('xmlns:components',self.ns)[0].findall('xmlns:component',self.ns):
			if (component.attrib['name']==component_name):
				return component

	def find_component_by_name(self, component_name):
		component=self.find_component(component_name)
		if (component==[]):
			raise Exception('Component %s not found' % component_name)
		return component			
	
	def get_component_code(self,component_name):
		component=self.find_component_by_name(component_name)
		return int(component.attrib['id'])
		
	def find_state_machine_by_name(self,component,state_machine_name):
		state_machine=[]
		for stateMachines in component.findall('xmlns:stateMachines',self.ns):
			for stateMach in stateMachines.findall('xmlns:stateMachine',self.ns):
				if (stateMach.attrib['name']==state_machine_name):
					state_machine=stateMach
		if (state_machine==[]):
			raise Exception('State Machine %s not found' % state_machine_name)
		return state_machine
		
	def get_state_machine_code(self,component_name,state_machine_name):
		component=self.find_component_by_name(component_name)
		state_machine=self.find_state_machine_by_name(component,state_machine_name)
		return int(state_machine.attrib['id'])

	def get_publisher(self,component_code,state_machine_code,message_type):
		for publish in ((self.root).findall('xmlns:clientAPICommunication',self.ns))[0].findall('xmlns:publish',self.ns):
			if ((int(publish.attrib['componentCode'])==component_code) and (int(publish.attrib['stateMachineCode'])==state_machine_code) and (publish.attrib['event']==message_type)):
				return publish

	def get_publisher_details(self,component_code,state_machine_code,message_type):
		publish=self.get_publisher(component_code,state_machine_code,message_type)
		if (publish=={}):
			raise Exception('publisher not found - component code : %i - statemachine code : %i - message type : %s' % (component_code,state_machine_code,message_type))
		return {'eventCode':int(publish.attrib['eventCode']),'routingKey':publish.findall('xmlns:topic',self.ns)[0].text}
		
	def get_subscriber(self,component_code,state_machine_code,event_type):
		for subscribe in ((self.root).findall('xmlns:clientAPICommunication',self.ns))[0].findall('xmlns:subscribe',self.ns):
			if ((int(subscribe.attrib['componentCode'])==component_code) and (int(subscribe.attrib['stateMachineCode'])==state_machine_code) and ((subscribe.attrib['eventType']).upper==event_type)):
				return subscribe
	
	def get_subscriber_topic(self,component_code,state_machine_code,event_type):
		subscribe=self.get_subscriber(component_code,state_machine_code,event_type)
		if (subscriber==[]):
			raise Exception('Subscriber not found - component code: %i - statemachine code: %i' % (component_code,state_machine_code))
		return subscribe.findall('xmlns:topic',self.ns)[0].text
		
	def get_fsharp_format(self,value):
		return {"Case":"Some", "Fields":[value]}

	def get_header_config(self,component_code,state_machine_code,message_type):
		return {"StateMachineCode":self.get_fsharp_format(state_machine_code),
				"ComponentCode":self.get_fsharp_format(component_code),
				"EventCode":self.get_publisher_details(component_code,
													   state_machine_code,
													   message_type)["eventCode"],
				"IncomingType":0,
				"MessageType":self.get_fsharp_format(message_type)}
    
	def get_routing_key(self,component_code,state_machine_code,message_type):
		publish=self.get_publisher_details(component_code,state_machine_code,message_type)
		return publish['routingKey']
	
	def get_data_to_send(self,component_name,state_machine_name,message_type,json_message):
		component_code=self.get_component_code(component_name)
		state_machine_code=self.get_state_machine_code(component_name,state_machine_name)
		header_config=self.get_header_config(component_code,state_machine_code,message_type)
		routing_key=self.get_routing_key(component_code,state_machine_code,message_type)
		return {"RoutingKey":routing_key,"ComponentCode":component_code, "Event":{"Header":header_config,"JsonMessage":json.dumps(json_message)}}

	def sender(self,component_name,state_machine_name,message_type,json_message):
		data=self.get_data_to_send(component_name,state_machine_name,message_type,json_message)
		self.web_socket_input=serializer.convert_to_websocket_input_format(data)
		self.websocket.send(self.web_socket_input)
