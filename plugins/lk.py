from time import *


netpack_plugin = True

class Logic():
    name = "lk"
    desc = "Lower Kurast 3ppl chest bot. Type \\lk help for more information."
    hlp = (
        "\\lk help",
        "\\lk start sorcname mule1 mule2"
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
