import imp
import os


class LogicElement():
    def __init__(self,

class PluginManager():
    def __init__(self):
        self.plugins = ()
        self.logics = ()
        plugdir = ".\\plugins"
        for fname in os.listdir(plugdir):
            if os.path.isfile(plugdir + "\\" + fname):
                mname, ext = os.path.splitext(fname)
                if ext == ".py":
                    file, pathname, desc = imp.find_module(mname, [plugdir])
                    m = imp.load_module(mname, file, pathname, desc)
                    if "netpack_plugin" in dir(m):
                        self.plugins = self.plugins + (m.Logic,)

    def callback

pm = PluginManager()
