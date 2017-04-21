from reactivexcomponent.communication.xcConnection import *

class xcomponentAPI:
	
	def create_session(self,xc_api,serverURL,callback):
		self.connection=xcConnection()
		self.connection.create_connection(xc_api,serverURL,callback)
