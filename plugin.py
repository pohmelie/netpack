import imp
import os
from d2crypt import Decrypter, encrypt

'''from multiprocessing import log_to_stderr, SUBDEBUG
import logging
logger = log_to_stderr()
#logger.setLevel(logging.WARNING)
logger.setLevel(SUBDEBUG)'''

iscommand = lambda data: data[0] == 0x15 and str(data[3:4], "ascii") == "\\"
getcommand = lambda data: str(data[3: -3], "ascii")

class PluginManager():
    def __init__(self):
        self.plugins = ()
        plugdir = ".\\plugins"
        for fname in os.listdir(plugdir):
            if os.path.isfile(plugdir + "\\" + fname):
                mname, ext = os.path.splitext(fname)
                if ext == ".py":
                    file, pathname, desc = imp.find_module(mname, [plugdir])
                    m = imp.load_module(mname, file, pathname, desc)
                    if "netpack_plugin" in dir(m):
                        self.plugins = self.plugins + (m.Logic,)

    def check_for_charname(self, packs):
        for pack in packs:
            if pack[0] == 0x59: #assign player
                p = self.ps.funcs[PluginManager.SERVER][pack[0]].unpack(pack)
                if p["x"] == 0 and p["y"] == 0:
                    return "".join(map(chr, filter(bool, p["Char Name"])))
