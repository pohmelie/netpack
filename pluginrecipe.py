from connection import Connection
from threading import Thread
from time import sleep
from au3bind import autoit
from construct import *


def echo(pack, cname):
    return info(
        str(pack.message, "ascii"),
        "white",
        "open_chat",
        bytes(cname, "ascii")
    )

def info(s, col="silver", ctype="system", cname=b"[sys]"):
    return([
        Container(
            fun = "chat",
            entity_id = 0,
            entity_type = "stash_wp_portal_chest",
            chat_type = ctype,
            color = col,
            char_level = 0,
            message = bytes(s, "ascii"),
            char_name = cname,
            start_fun = 0
        )],
        Connection.SERVER,
        Connection.CLIENT
    )

def check_command(pack):
    return \
        pack.fun == "send_normal_chat" and \
        pack.mode == "normal" and \
        str(pack.message, encoding="ascii")[0] == "\\"

class Rejoiner(Thread):
    def __init__(self, caption, gamename, gamepass):
        Thread.__init__(self)

        self.caption = caption
        self.gamename = gamename
        self.gamepass = gamepass

    def run(self):
        self.au3 = autoit()
        self.au3.AU3_ControlSend(self.caption, "", "", "{ESCAPE}")
        self.au3.AU3_ControlClick(self.caption, "", "", "left", 1, 400, 260)
        sleep(3)
        self.au3.AU3_ControlClick(self.caption, "", "", "left", 1, 590, 460)
        sleep(1)
        self.au3.AU3_ControlSend(self.caption, "", "", self.gamename + "{TAB}" + self.gamepass + "{ENTER}")

