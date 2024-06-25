from enum import Enum


class ClientStatusEnum(str, Enum):
    INITIALIZING = "INITIALIZING"
    CONNECTING_TO_LOGIN_SERVER = "CONNECTING_TO_LOGIN_SERVER"
    LOGIN_TIMED_OUT = "LOGIN_TIMED_OUT"
    AUTHENTICATING_TO_LOGIN_SERVER = "AUTHENTICATING_TO_LOGIN_SERVER"
    BANNED = "BANNED"
    AUTHENTICATED_TO_LOGIN_SERVER = "AUTHENTICATED_TO_LOGIN_SERVER"
    GAME_SERVERS_LIST_RECEIVED = "GAME_SERVERS_LIST_RECEIVED"
    SELECTING_SERVER = "SELECTING_SERVER"
    SERVER_SELECTION_IMPOSSIBLE = "SERVER_SELECTION_IMPOSSIBLE"
    SERVER_SELECT_SUCCESS = "SERVER_SELECT_SUCCESS"
    SERVER_SELECT_FAILED = "SERVER_SELECT_FAILED"
    SWITCHING_TO_GAME_SERVER = "CONNECTING_TO_GAME_SERVER"
    CONNECTED_TO_GAME_SERVER = "CONNECTED_TO_GAME_SERVER"
    AUTHETICATING_TO_GAME_SERVER = "AUTHETICATING_TO_GAME_SERVER"
    AUTHETICATED_TO_GAME_SERVER = "AUTHENTICATED_TO_GAME_SERVER"
    CHARACTERS_LIST_RECEIVED = "CHARACTERS_LIST_RECEIVED"
    SELECTING_CHARACTER = "SELECTING_CHARACTER"
    CHARACTER_SELECTION_FAILED = "CHARACTER_SELECTION_FAILED"
    CHARACTER_SELECTED = "CHARACTER_SELECTED"
    GAME_SESSION_STARTED = "GAME_SESSION_STARTED"
    LOADING_MAP = "LOADING_MAP"
    REQUESTING_MAP_DATA = "REQUESTING_MAP_DATA"
    MAP_DATA_RECEIVED = "MAP_DATA_RECEIVED"
    PROCESSING_MAP_DATA = "PROCESSING_MAP"
    MAP_DATA_PROCESSED = "MAP_DATA_PROCESSED"
    CHANGING_CONTEXT = "CHANGING_CONTEXT"
    SWITCHED_TO_FIGHTING = "FIGHTING"
    SWITCHED_TO_ROLEPLAY = "ROLEPLAYING"
    OUT_OF_ROLEPLAY = "OUT_OF_ROLEPLAY"
    CONNECTION_CLOSED = "CONNECTION_CLOSED"
    CRASHED = "CRASHED"
    DISCONNECTED = "DISCONNECTED"
    IDLE = "IDLE"
    STOPPING = "STOPPING"
    TERMINATED = "TERMINATED"

    # extra for testing purposes maybe later integrate it into the main code
    USING_INTERACTIVE = "USING_INTERACTIVE"
    INTERACTIVE_USE_FAILED = "INTERACTIVE_FAILED"
    INTERACTIVE_SUCCESS = "INTERACTIVE_SUCCESS"

    USING_ITEM = "USING_ITEM"
    ITEM_USE_FAILED = "ITEM_USE_FAILED"
    ITEM_USE_SUCCESS = "ITEM_USE_SUCCESS"

    DIALOG_WITH_NPC = "DIALOG_WITH_NPC"
    DIALOG_WITH_NPC_ENDED = "DIALOG_WITH_NPC_ENDED"

    EXCHANGING_WITH_PLAYER = "EXCHANGING_WITH_PLAYER"
    EXCHANGE_FAILED = "EXCHANGE_FAILED"
    EXCHANGE_SUCCESS = "EXCHANGE_SUCCESS"

    INTERACTING_WITH_BANK_STORAGE = "INTERACTING_WITH_BANK_STORAGE"
    BANK_STORAGE_INTERACTION_FAILED = "BANK_STORAGE_INTERACTION_FAILED"
    BANK_STORAGE_INTERACTION_SUCCESS = "BANK_STORAGE_INTERACTION_SUCCESS"

    REQUESTING_MAP_MOVEMENT = "REQUESTING_MAP_MOVEMENT"
    MOVEMENT_IN_PROGRESS = "MOVEMENT_IN_PROGRESS"
    MOVEMENT_REJECTED = "MOVEMENT_REJECTED"
    MOVEMENT_COMPLETED = "MOVEMENT_COMPLETED"

    CHANGING_MAP = "CHANGING_MAP"
    MAP_CHANGE_FAILED = "MAP_CHANGE_FAILED"
    MAP_CHANGE_SUCCESS = "MAP_CHANGE_SUCCESS"
