class ChatActivableChannelsEnum:

    CHANNEL_GLOBAL = 0

    CHANNEL_TEAM = 1

    CHANNEL_GUILD = 2

    CHANNEL_ALLIANCE = 3

    CHANNEL_PARTY = 4

    CHANNEL_SALES = 5

    CHANNEL_SEEK = 6

    CHANNEL_NOOB = 7

    CHANNEL_ADMIN = 8

    CHANNEL_ADS = 12

    CHANNEL_ARENA = 13

    CHANNEL_COMMUNITY = 14

    PSEUDO_CHANNEL_PRIVATE = 9

    PSEUDO_CHANNEL_INFO = 10

    PSEUDO_CHANNEL_FIGHT_LOG = 11

    @classmethod
    def to_name(cls, value):
        for k, v in vars(cls).items():
            if v == value:
                return k
        return None
