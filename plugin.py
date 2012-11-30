import imp
import os
from functools import partial
from connection import *
from d2packet import PacketSplitter
from d2crypt import decrypt, encrypt
from itertools import chain


class LogicElement():
    def __init__(self, name=None, con=None, logic=None):
        self.name = name
        self.con = con
        self.logic = logic

class PluginManager():
    def __init__(self):
        self.plugins = ()
        self.logics = {}
        self.ps = PacketSplitter()
        plugdir = ".\\plugins"
        for fname in os.listdir(plugdir):
            if os.path.isfile(plugdir + "\\" + fname):
                mname, ext = os.path.splitext(fname)
                if ext == ".py":
                    file, pathname, desc = imp.find_module(mname, [plugdir])
                    m = imp.load_module(mname, file, pathname, desc)
                    if "netpack_plugin" in dir(m):
                        self.plugins = self.plugins + (m.Logic,)

    @staticmethod
    def iscommand(data):
        return data[0] == 0x15 and str(data[3:4], "ascii") == "\\"

    @staticmethod
    def getcommand(data):
        return str(data[3: -3], "ascii")

    @staticmethod
    def encryptp(p):
        return (p[0], tuple(map(encrypt, p[1])))

    def check_for_charname(self, packs):
        for pack in packs:
            if pack[0] == 0x59: #assign player
                p = self.ps.funcs[Connection.SERVER][pack[0]].unpack(pack)
                if p["x"] == 0 and p["y"] == 0:
                    return "".join(map(chr, filter(bool, p["Char Name"])))

    def pluglogic(self, con, packs):
        drop = False
        ret = tuple(filter(lambda x: not iscommand(x), packs))
        for pack in filter(iscommand, packs):
            drop = True
            com = getcommand(data).lower()
            if com.startswith("\\init"):
                pass #window naming and plug list
            else:
                com = com.split()
                com, params = com[0], tuple(com[1:])
                for plug in self.plugins:
                    if "\\" + plug.name == com:
                        for le in self.logics.values():
                            if le.con == con:
                                le.logic = plug()
                                break
                        break
        return drop, (ret, ())

    def idle(self, con):
        pass

    def callback(self, con, data, s, d):
        drop, fake = False, ((), ())
        if s == Connection.SERVER:
            try:
                data = decrypt(data)
            except:
                pass
        packs = self.ps.split(data, s)
        if s == Connection.SERVER:
            cname = self.check_for_charname(packs)
            if cname:
                self.logics[cname] = self.logics.get(cname, LogicElement(cname))
                self.logics[cname].con = con
        for le in self.logics.values():
            if le.con == con and le.logic:
                stop, drop, fake = le.logic.callback(packs)
                if stop:
                    le.logic = None
                break
        else:
            if s == Connection.CLIENT:
                drop, fake = self.pluglogic(con, packs)
        return drop, self.encryptp(fake)

'''
def defaultlogic(self, con, data, s, d):
        if s == Connection.CLIENT and Logic.iscommand(data):
            command = Logic.getcommand(data).lower()
            if command.startswith == "\\init":
                logic = Logic()
                con.callback = logic.callback
                self.logics = self.logics + (logic,)
            elif command.startswith("\\bot"):
                try:
                    w, n = tuple(command.split())
                    for logic in self.logics:
                        if logic.lid == int(n) - 1:
                            con.callback = logic.callback
                            break
                except:
                    pass
            return True, ((), (b"",))
        else:
            return False, ((), ())'''
