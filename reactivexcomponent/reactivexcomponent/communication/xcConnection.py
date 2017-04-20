from reactivexcomponent.communication.xcSession import *

class xcConnection:
	
	def createSession(self,xcAPI,serverURL,callback):
		self.session=xcSession()
		self.session.init(xcAPI,serverURL,callback)
