import imp
import os
from d2crypt import decrypt, encrypt


def get_plugins():
    plugins = ()
    plugdir = ".\\plugins"
    for fname in os.listdir(plugdir):
        if os.path.isfile(plugdir + "\\" + fname):
            mname, ext = os.path.splitext(fname)
            if ext == ".py":
                file, pathname, desc = imp.find_module(mname, [plugdir])
                m = imp.load_module(mname, file, pathname, desc)
                if "netpack_plugin" in dir(m):
                    plugins = plugins + (m.Logic,)
    return plugins

class LogicElement():
    def __init__(self, name=None, con=None, logic=None):
        self.name = name
        self.con = con
        self.logic = logic

iscommand = lambda data: data[0] == 0x15 and str(data[3:4], "ascii") == "\\"
getcommand = lambda data: str(data[3: -3], "ascii")

def defaultpluginloop(qi, qo):
    def clojure():
        while True:
            data, _, _, _, _ = qi.get()
            logger.debug(data)
            qo.put_nowait(data)
    return clojure

def pluginloop(qi, qo, plugins, splitter):
    while True:
        data, s, d, qi, qo = qi.get()
        qo.put_nowait(data)

def check_for_charname(packs):
    for pack in packs:
        if pack[0] == 0x59: #assign player
            p = self.ps.funcs[PluginManager.SERVER][pack[0]].unpack(pack)
            if p["x"] == 0 and p["y"] == 0:
                return "".join(map(chr, filter(bool, p["Char Name"])))

def pluglogic(self, con, packs):
    drop = False
    for pack in filter(PluginManager.iscommand, packs):
        drop = True
        com = PluginManager.getcommand(pack).lower()
        if com.startswith("\\help"):
            pass #window naming and plug list
        else:
            com = com.split()
            logger.debug(com)
            com, params = com[0], tuple(com[1:])
            for plug in self.plugins:
                logger.debug(plug.name)
                if "\\" + plug.name == com:
                    for le in self.logics.values():
                        if le.con == con:
                            le.logic = plug(*params)
                            break
                    break
    if drop:
        ret = tuple(filter(lambda x: not PluginManager.iscommand(x), packs))
    else:
        ret = ()
    return drop, (ret, (b"",))

def idle(self):
    pass
    #for le in self.logics.values():
    #    stop, fake = le.logic.idle()

def callback(self, con, data, s, d):
    drop, fake = False, ((), ())
    if s == PluginManager.SERVER:
        try:
            data = decrypt(data)
        except:
            pass
    packs = self.ps.split(data, s)
    if s == PluginManager.SERVER:
        cname = self.check_for_charname(packs)
        if cname:
            self.logics[cname] = self.logics.get(cname, LogicElement(cname))
            self.logics[cname].con = con
    for le in self.logics.values():
        if le.con == con and le.logic:
            stop, drop, fake = le.logic.callback(packs, s, d)
            if stop:
                le.logic = None
            break
    else:
        if s == PluginManager.CLIENT:
            drop, fake = self.pluglogic(con, packs)

    self.logics = dict(filter(lambda x: x[1].logic != None, self.logics.items()))
    return drop, self.encryptp(fake)
