import os
from subprocess import Popen, PIPE
import json
from time import sleep
import httpx
from com.ankamagames.jerakine.logger.Logger import Logger
from com.ankamagames.jerakine.metaclasses.Singleton import Singleton
import xml.etree.ElementTree as ET

logger = Logger("Dofus2")
from launcher.AccountCredsManager import AccountCredsManager


class Haapi(metaclass=Singleton):
    def __init__(self) -> None:
        self.url = "https://haapi.ankama.com"
        self.APIKEY = None

    def getUrl(self, request):
        return (
            self.url
            + {
                "CREATE_API_KEY": "/json/Ankama/v5/Api/CreateApiKey",
                "GET_LOGIN_TOKEN": "/json/Ankama/v5/Account/CreateToken",
            }[request]
        )

    def createAPIKEY(self, accountId, game_id=102) -> str:
        logger.debug("Calling HAAPI to Create APIKEY")
        creds = AccountCredsManager.getEntry(accountId)
        cert = self.getCert(creds["login"])
        data = {
            "login": creds["login"],
            "password": creds["password"],
            "game_id": game_id,
            "long_life_token": True,
            "certificate_id": cert["id"],
            "certificate_hash": cert["hash"],
            "shop_key": "ZAAP",
            "payment_mode": "OK",
        }
        response = httpx.post(
            self.getUrl("CREATE_API_KEY"),
            data=data,
            headers={
                "User-Agent": "Zaap",
                "Content-Type": "multipart/form-data",
            },
        )
        self.APIKEY = response.json()["key"]
        logger.debug("APIKEY created")
        return self.APIKEY

    def getCert(self, login):
        CURRDIR = os.path.dirname(__file__)
        p = Popen(
            ["cd", CURRDIR, "&&", "node", "getCertificate.js", login],
            stderr=PIPE,
            stdout=PIPE,
            shell=True,
        )
        stdout, stderr = p.communicate()
        if stderr:
            raise Exception(stderr.decode("utf-8"))
        ret_json = stdout.decode("utf-8")
        cert = json.loads(ret_json)
        logger.debug("Certificate loaded")
        return cert

    def getLoginToken(self, accountId, game_id=1):
        logger.debug("Calling HAAPI to get Login Token")
        if not self.APIKEY:
            self.createAPIKEY(accountId)
        creds = AccountCredsManager.getEntry(accountId)
        cert = self.getCert(creds["login"])
        nbrTries = 0
        while nbrTries < 3:
            response = httpx.get(
                self.getUrl("GET_LOGIN_TOKEN"),
                params={
                    "game": game_id,
                    "certificate_id": cert["id"],
                    "certificate_hash": cert["hash"],
                },
                headers={
                    "User-Agent": "Zaap1",
                    "Content-Type": "multipart/form-data",
                    "APIKEY": self.APIKEY,
                },
            )
            try:
                token =  response.json()["token"]
                logger.debug("Login Token created")
                return token
            except json.decoder.JSONDecodeError as e:
                from bs4 import BeautifulSoup

                parsed_html = BeautifulSoup(response.content)
                reason = parsed_html.body.find("div", attrs={"id": "what-happened-section"}).find("p").text
                if (
                    reason
                    == "The owner of this website (haapi.ankama.com) has banned you temporarily from accessing this website."
                ):
                    logger.debug("Login Token creation failed, reason: %s" % reason)
                    logger.debug("Retrying in 60 seconds")
                    sleep(60)

        


if __name__ == "__main__":
    myAccountId = "149512160"
    haapi = Haapi()
    print("LOGIN Token " + haapi.getLoginToken(myAccountId))
