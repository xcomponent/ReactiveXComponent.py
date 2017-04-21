""" Session """

import ssl
import websocket as WebSocket
from reactivexcomponent.communication.publisher import *

class xcSession:
		
	def init(self,xc_api, server_url,callback):
		self.xc_api=xc_api
		self.websocket = WebSocket.WebSocketApp(server_url)
                              
		def on_open(websocket):
		   callback(0,self)
		
		def on_error(websocket,error):
			callback(error,0)

		def on_close(websocket):
			print('### session %s closed ###' % server_url)
			
			
		self.websocket.on_open = on_open
		self.websocket.on_error = on_error
		self.websocket.on_close = on_close
		
		self.websocket.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})

	def create_publisher(self):
		p=Publisher()
		p.file=self.xc_api
		p.get_xml_content()
		p.websocket=self.websocket
		return p
