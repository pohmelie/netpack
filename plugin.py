import imp
import os
from d2crypt import Decrypter, encrypt
from d2packetparser import d2_packet_parser
from multiprocessing import Process
from connection import Connection
from construct import *


import multiprocessing, logging
logger = multiprocessing.log_to_stderr()
logger.setLevel(logging.WARNING)

def info(s, col="silver"):
    return([
        Container(
            fun = "chat",
            entity_id = 0,
            entity_type = "stash_wp_portal_chest",
            chat_type = "system",
            color = col,
            char_level = 0,
            message = bytes(s, "ascii"),
            char_name = b"[sys]",
            start_fun = 0
        )],
        Connection.SERVER,
        Connection.CLIENT
    )

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
                    if src == Connection.SERVER:
                        odata = encrypt(odata)
                    self.qo.put((odata, src, dst))

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

    def act(self, packets, s, d):
        return (packets, s, d)
        #info("packets {}".format(self.deb))
