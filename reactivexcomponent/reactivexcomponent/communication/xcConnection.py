""" Create Connection """

from reactivexcomponent.communication.xcSession import *

class xcConnection:
	
	def create_connection(self,xc_api,server_url,callback):
		self.session=xcSession()
		self.session.init(xc_api,server_url,callback)
