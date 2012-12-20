import imp
import os
from d2crypt import Decrypter, encrypt
from d2packetparser import d2_packet_parser
from multiprocessing import Process
from connection import Connection
from plugin_recipe import *
from recipe import *


from time import time
import multiprocessing, logging
logger = multiprocessing.log_to_stderr()
logger.setLevel(multiprocessing.SUBDEBUG)
#logger.setLevel(logging.WARNING)


class DefaultQueueControl(Process):
    def __init__(self, qi, qo):
        Process.__init__(self)
        self.dec = Decrypter()
        self.qi = qi
        self.qo = qo

    def run(self):
        self.plug = PluginManager()
        while True:
            data, s, d = self.qi.get()
            mdata = (data,)
            if s == Connection.SERVER and data != b"\xaf\x01":
                mdata = self.dec.decrypt(data)
            for idata in mdata:
                for odata, src, dst in self.plug.act(d2_packet_parser[s].parse(idata), s, d):
                    odata = d2_packet_parser[src].build(odata)
                    if src == Connection.SERVER and data != b"\xaf\x01":
                        odata = encrypt(odata)
                    self.qo.put((odata, src, dst))

class PluginManager():
    def __init__(self):

        #self.f = open("log.txt", "w")

        self.welcome = info("Welcome to netpack. Type \\? or \\help for more information.", "green")
        self.plugins = ()
        self.hlp = ()
        self.plug = None
        self.char_name = None
        self.au3 = windll

        plugdir = ".\\plugins"
        for fname in os.listdir(plugdir):
            if os.path.isfile(plugdir + "\\" + fname):
                mname, ext = os.path.splitext(fname)
                if mname != "recipe" and ext == ".py":
                    file, pathname, desc = imp.find_module(mname, [plugdir])
                    m = imp.load_module(mname, file, pathname, desc)
                    if "netpack_plugin" in dir(m):
                        self.plugins = self.plugins + (m.Logic,)
                        self.hlp = self.hlp + (m.Logic.name + " - " + m.Logic.desc,)

    def act(self, packets, s, d):

        '''self.f.write("\n\n[{:.2f}] ".format(time() % 60))
        self.f.write(("c -> s", "s -> c")[s])
        for pack in packets:
            self.f.write("\n" + repr(pack))
        self.f.flush()'''

        real = []
        fake = []
        for pack in packets:
            if pack.fun == "send_logon_info" and s == Connection.CLIENT:
                self.char_name = str(pack.char_name, "ascii")
                real.append(pack)
            elif self.char_name and pack.fun == "player_in_game" and \
                s == Connection.SERVER and self.char_name == str(pack.char_name, "ascii"):
                fake.append(self.welcome)
                real.append(pack)
            elif check_command(pack):
                if self.char_name:
                    com = str(pack.message, "ascii").lower().split()
                    fword = com[0]
                    if fword in ("\\help", "\\?"):
                        fake.append(echo(pack, self.char_name))
                        fake.append(info("Netpack available plugins:", "br_white"))
                        apply(lambda x: fake.append(info(x)), self.hlp)
                        fake.append(info("Type '\\plugname help' for more information", "br_white"))

                    elif fword == "\\stop":
                        fake.append(echo(pack, self.char_name))
                        fake.append(info("plugin stopped"))
                        self.plug = None

                    elif fword == "\\name":
                        fake.append(echo(pack, self.char_name))

                        fake.append(info("you want name"))
                    else:
                        fake.append(info("you want extra"))
                        pass
                        #check plugins
                else:
                    fake.append(info("Netpack not ready, reconnect please.", "red"))
            else:
                real.append(pack)

        return [(real, s, d)] + fake
