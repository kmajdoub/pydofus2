class ServerConnectionErrorEnum:
    SERVER_CONNECTION_ERROR_DUE_TO_STATUS = 0
    SERVER_CONNECTION_ERROR_NO_REASON = 1
    SERVER_CONNECTION_ERROR_SUBSCRIBERS_ONLY = 3
    SERVER_CONNECTION_ERROR_REGULAR_PLAYERS_ONLY = 4
    SERVER_CONNECTION_ERROR_MONOACCOUNT_CANNOT_VERIFY = 5
    SERVER_CONNECTION_ERROR_MONOACCOUNT_ONLY = 6
    SERVER_CONNECTION_ERROR_SERVER_OVERLOAD = 7

    def __init__(self):
        super().__init__()
