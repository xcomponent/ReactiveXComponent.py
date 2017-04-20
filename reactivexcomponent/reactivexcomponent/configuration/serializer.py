import json

class serializer:
        def convertToWebsocketInputFormat(data):
                winput='{0} {1} {2}'.format(data['RoutingKey'],data['ComponentCode'],json.dumps(data['Event']))
                return winput
	
