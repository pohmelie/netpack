import imp
import os
from d2crypt import Decrypter, encrypt
from d2packetparser import d2_packet_parser
from multiprocessing import Process
from connection import Connection
from pluginrecipe import *
from recipe import *
from au3bind import autoit


from time import time
'''import multiprocessing, logging
logger = multiprocessing.log_to_stderr()
logger.setLevel(multiprocessing.SUBDEBUG)'''
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
            x = self.qi.get()
            if x == None:
                self.qo.put(None)
                continue
            data, s, d = x
            #logger.warning(repr(data))
            #logger.warning("in: " + rev(data))
            mdata = (data,)
            if s == Connection.SERVER and data != b"\xaf\x01":
                mdata = self.dec.decrypt(data)
            for idata in mdata:
                for odata, src, dst in self.plug.act(d2_packet_parser[s].parse(idata), s, d):
                    odata = d2_packet_parser[src].build(odata)
                    if src == Connection.SERVER and data != b"\xaf\x01":
                        odata = encrypt(odata)
                    #logger.warning("out: " + rev(odata))
                    self.qo.put((odata, src, dst))

class PluginManager():
    builtins_help = (
        "\\? or \\help - this message.",
        "\\name [caption] - sets window caption to [caption] (character name if omitted).",
        "\\start plugname - starts 'plugname' plugin.",
        "\\stop - stops current plugins."
    )

    def __init__(self):

        self.f = open("log.txt", "w")

        self.welcome = info("Welcome to netpack. Type \\? or \\help for more information.", "green")
        self.plugins = ()
        self.hlp = ()
        self.plugs = ()
        self.char_name = None
        self.au3 = autoit()

        for fname in os.listdir("."):
            if os.path.isfile(fname):
                mname, ext = os.path.splitext(fname)
                if mname.startswith("plugin_") and ext == ".py":
                    file, pathname, desc = imp.find_module(mname)
                    m = imp.load_module(mname, file, pathname, desc)
                    if "netpack_plugin" in dir(m):
                        self.plugins = self.plugins + (m.Logic,)
                        self.hlp = self.hlp + (m.Logic.name + " - " + m.Logic.desc,)

    def act(self, packets, s, d):

        self.f.write("\n\n[{:.2f}] ".format(time() % 60))
        self.f.write(("c -> s", "s -> c")[s])
        for pack in packets:
            self.f.write("\n" + repr(pack))
        self.f.flush()

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
                        fake.append(info("Netpack builtins:", "br_white"))
                        apply(lambda x: fake.append(info(x)), self.builtins_help)
                        fake.append(info("Netpack available plugins:", "br_white"))
                        apply(lambda x: fake.append(info(x)), self.hlp or ("None",))
                        fake.append(info("Currently running plugins:", "br_white"))
                        if self.plugs:
                            apply(lambda x: fake.append(info(x.name)), self.plugs)
                        else:
                            fake.append(info("None"))

                    elif fword == "\\start":
                        fake.append(echo(pack, self.char_name))
                        if len(com) > 1:
                            pname = com[1]
                            for p in self.plugins:
                                if p.name == pname:
                                    self.plugs = self.plugs + (p(self.char_name),)
                                    fake.append(info("'{}' plugin added to queue.".format(pname)))
                                    break
                            else:
                                fake.append(info("There is no '{}' plugin.".format(com[1]), "red"))
                        else:
                            fake.append(info("Wrong input. Type \\? or \\help for more information.", "red"))

                    elif fword == "\\stop":
                        fake.append(echo(pack, self.char_name))
                        if self.plugs:
                            fake.append(info("{} plugins stopped.".format(len(self.plugs))))
                            self.plugs = ()
                        else:
                            fake.append(info("There are no running plugins.", "red"))

                    elif fword == "\\name":
                        fake.append(echo(pack, self.char_name))
                        name = self.char_name
                        if len(com) > 1:
                            name = com[1]
                        self.au3.AU3_WinSetTitle("", "", name)
                        fake.append(info("Window caption set to '{}'".format(name)))

                    else:
                        real.append(pack)
                else:
                    fake.append(info("Netpack is not ready, reconnect please.", "red"))
            else:
                real.append(pack)

        for p in self.plugs:
            real, f = p.act(real, s, d)
            fake = fake + f
        return [(real, s, d)] + fake
