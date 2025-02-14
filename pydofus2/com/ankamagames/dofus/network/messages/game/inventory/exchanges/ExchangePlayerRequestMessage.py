from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.exchanges.ExchangeRequestMessage import (
    ExchangeRequestMessage,
)


class ExchangePlayerRequestMessage(ExchangeRequestMessage):
    target: int

    def init(self, target_: int, exchangeType_: int):
        self.target = target_

        super().init(exchangeType_)
