from time import *
from pluginrecipe import *
from au3bind import autoit
from construct import *
from connection import Connection


netpack_plugin = True
class Logic():
    name = "lk"
    desc = "Lower Kurast 3ppl chest bot. Type \\lk help for more information."
    hlp = (
        "\\lk help - this message.",
        "\\lk set sorc mule1 mule2 - sets windows captions for sorc and mules."
        "\\lk start",
        "\\lk stop"
    )

    def __init__(self):
        self.sorc = self.mule1 = self.mule2 = None
        self.runs = 0
        self.act = self.waiting_game_enter

        self.au3 = autoit()
        Rejoiner("catfish", "yoba", "yoba").start()

    def waiting_game_enter(self, packets, s, d):
        fake = []
        if s == Connection.SERVER:
            for pack in packets:
                if pack.fun == "player_in_game":
                    fake.append(info("i'm in game, baby!"))
        return packets, fake
