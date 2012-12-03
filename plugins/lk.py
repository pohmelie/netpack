from time import *
from ctypes import *


netpack_plugin = True

class Logic():
    name = "lk"
    desc = "Lower Kurast 3ppl chest bot\nUsage: \\lk sorcname mulename mulename"

    def __init__(self, *args):
        self.sorcname = args[0]
        self.mulenames = args[1:]
        au3 = windll.AutoItX3
        logger.debug("i'm here")

    def callback(self, packs, s, d):
        ret = [(), ()]
        ret[s] = packs
        au3.WinSetTitle("", "", strftime("%H:%M:%S"))
        logger.debug("i'm here in callback")
        return False, True, tuple(ret)

    def idle(self):
        pass

import multiprocessing, logging
logger = multiprocessing.log_to_stderr()
logger.setLevel(multiprocessing.SUBDEBUG)
