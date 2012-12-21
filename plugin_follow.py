from time import *


netpack_plugin = True

class Logic():
    name = "follow"
    desc = "simple follow bot."
    hlp = (
        "\\follow help",
    )

    def __init__(self, *args):
        self.sorcname = args[0]
        self.mulenames = args[1:]
        au3 = windll.AutoItX3

    def act(self, packets, s, d):
        ret = [(), ()]
        ret[s] = packs
        au3.WinSetTitle("", "", strftime("%H:%M:%S"))
        return False, True, tuple(ret)
