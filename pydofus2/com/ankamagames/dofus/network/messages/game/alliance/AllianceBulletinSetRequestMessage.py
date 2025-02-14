from pydofus2.com.ankamagames.dofus.network.messages.game.social.SocialNoticeSetRequestMessage import (
    SocialNoticeSetRequestMessage,
)


class AllianceBulletinSetRequestMessage(SocialNoticeSetRequestMessage):
    content: str

    def init(self, content_: str):
        self.content = content_

        super().init()
