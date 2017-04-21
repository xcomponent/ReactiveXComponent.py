from reactivexcomponent.communication.xcSession import *
from reactivexcomponent.xcomponentAPI import *

def callback(error,session):
    if error!=0:
        print('erreur')
        return
    publish=session.create_publisher()
    publish.sender('Devinette','DevinetteChecker','XComponent.Devinette.UserObject.CheckWord',{})
    
xc_api_file="data\\WebSocket_NewDevinetteApi_test.xcApi"
server_url="wss://localhost:443"
xc_api=xcomponentAPI()
xc_api.create_session(xc_api_file,server_url,callback)
