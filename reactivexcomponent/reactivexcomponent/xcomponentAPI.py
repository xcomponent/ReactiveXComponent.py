from reactivexcomponent.communication.xcConnection import *

class xcomponentAPI:
	
	def createSession(self,xcAPI,serverURL,callback):
		self.connection=xcConnection()
		self.connection.createSession(xcAPI,serverURL,callback)
