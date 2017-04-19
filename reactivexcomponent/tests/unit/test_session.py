from reactivexcomponent.communication.xcSession import *
from reactivexcomponent.xcomponentAPI import *

def callback(error,session):
    if error!=0:
        print('erreur')
        return
    publish=session.createPublisher()
    publish.sender('Devinette','DevinetteChecker','XComponent.Devinette.UserObject.CheckWord',{})
    
    
xcApiFile="WebSocket_NewDevinetteApi_test.xcApi"
serverURL="wss://localhost:443"
xcApi=xcomponentAPI()
xcApi.createSession(xcApiFile,serverURL,callback)
