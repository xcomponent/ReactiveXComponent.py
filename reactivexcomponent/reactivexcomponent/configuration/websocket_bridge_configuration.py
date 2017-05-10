
class EventType:

    Update = "UPDATE"

    Error = "ERROR"


class WebsocketTopicKind:

    Snapshot = 1

    Private = 2

    Public = 3


class Command:

    # pylint: disable=invalid-name
    hb = "hb"
    # pylint: enable=invalid-name

    update = "update"

    subscribe = "subscribe"

    get_xc_api = "getXcApi"

    get_xc_api_list = "getXcApiList"

    get_model = "getModel"
