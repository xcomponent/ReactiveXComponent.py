
class EventType:

    Update = "UPDATE"

    Error = "ERROR"


class WebsocketTopicKind:

    Snapshot = 1

    Private = 2

    Public = 3


class Command:

    heartbeat = "hb"

    update = "update"

    snapshot = "snapshot"

    subscribe = "subscribe"

    unsubscribe = "unsubscribe"

    get_xc_api = "getXcApi"

    get_xc_api_list = "getXcApiList"

    get_model = "getModel"
