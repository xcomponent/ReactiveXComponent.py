from ReactiveXComponent.communication.xcSession import *

class xcConnection:
	
	def createSession(self,xcAPI,serverURL,callback):
		print("xcConection",serverURL)
		self.session=xcSession()
		self.session.init(xcAPI,serverURL,callback)
