from reactivexcomponent.xcomponent_api import XcomponentAPI
from reactivexcomponent.communication.publisher import Publisher
from reactivexcomponent.communication.subscriber import Subscriber

def state_machine_update_listener(data):
    print(data)

def callback(error,session):
    if error is not None:
        print('erreur')
        return
    subscriber = session.create_subscriber()
    subscriber.subscribe('Devinette', 'DevinetteStatus', state_machine_update_listener)

    subscriber2 = session.create_subscriber()
    subscriber2.subscribe('Devinette', 'DevinetteStatus', state_machine_update_listener)
    subscriber2.dispose_observable_subscribers()

    subscriber3 = session.create_subscriber()
    subscriber3.subscribe('Devinette', 'Devinette', state_machine_update_listener)
    
xcApiFile="data\\WebSocket_NewDevinetteApi_test.xcApi"
serverURL="wss://localhost:443"
xcApi=XcomponentAPI()
xcApi.create_session(xcApiFile,serverURL,callback)
