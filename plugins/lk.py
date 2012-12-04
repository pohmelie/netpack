from time import *
from ctypes import *
from multiprocessing import Process, Queue


netpack_plugin = True

class Logic(Process):
    name = "lk"
    desc = "Lower Kurast 3ppl chest bot\nUsage: \\lk sorcname mulename mulename"

    def __init__(self, qi, qo, *args):
        Process.__init__(self)

        self.qi = qi
        self.qo = qo

        self.sorcname = args[0]
        self.mulenames = args[1:]
        au3 = windll.AutoItX3

    def run(self):
        while True:
            pass

    def callback(self, packs, s, d):
        ret = [(), ()]
        ret[s] = packs
        au3.WinSetTitle("", "", strftime("%H:%M:%S"))
        return False, True, tuple(ret)

    def idle(self):
        pass
