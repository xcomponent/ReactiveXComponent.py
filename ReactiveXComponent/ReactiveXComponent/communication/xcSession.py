import websocket as WebSocket
import ssl
from reactivexcomponent.communication.publisher import *

class xcSession:
		
	def init(self,xcAPI, serverURL,callback):
		self.xcAPI=xcAPI
		self.websocket = WebSocket.WebSocketApp(serverURL)
                              
		def on_open(websocket):
		   callback(0,self)
		
		def on_error(websocket,error):
			callback(error,0)

		def on_close(websocket):
			print('###session %s closed###' % serverURL)
			
			
		self.websocket.on_open = on_open
		self.websocket.on_error = on_error
		self.websocket.on_close = on_close
		
		self.websocket.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})

	def createPublisher(self):
		p=publisher()
		p.file=self.xcAPI
		p.getXmlContent()
		p.websocket=self.websocket
		return p
