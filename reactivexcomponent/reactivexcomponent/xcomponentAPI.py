from reactivexcomponent.communication.xcConnection import XcConnection

class XcomponentAPI:
	
	def create_session(self,xc_api,serverURL,callback):
		self.connection = XcConnection()
		self.connection.create_connection(xc_api,serverURL,callback)
