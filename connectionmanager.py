from time import time, sleep
from multiprocessing import Process, Queue
from d2packetparser_c2s import c2s_packets
from plugin import DefaultQueueControl
from connection import Connection, unstack
from recipe import *


class LogicElement():
    def __init__(self, name, con, logic, qi, qo):
        self.name = name
        self.con = con
        self.logic = logic
        self.qi = qi
        self.qo = qo

    def smth(self, val):
        return val in (self.name, self.con, self.logic, self.qi, self.qo)

    def __repr__(self):
        pps = "LogicElement(name = {}, con = {}, logic = {}, qi = {}, qo = {}"
        return pps.format(self.name, self.con, self.logic, self.qi, self.qo)

class ConnectionManager(Process):
    def __init__(self, qi, qo, server_ips):
        Process.__init__(self)
        self.qi = qi
        self.qo = qo
        self.server_ips = server_ips
        self.logics = set()
        self.remcon = set()

    def filter_logics(self):
        remlog = set()
        t = time()
        for log in self.logics:
            if log.con and log.con.state in (Connection.TIMEOUT, Connection.RESET):
                self.remcon.add((log.con, t))
                if log.name:
                    log.con = None
                else:
                    log.logic.terminate()
                    remlog.add(log)
        self.logics = self.logics - remlog
        self.remcon = set(tuple(filter(lambda x: t - x[1] < 10, self.remcon)))

    def idle(self):
        while self.qi.empty():
            self.filter_logics()
            for log in self.logics:
                if log.con:
                    apply(self.qo.put, log.con.idle())
            sleep(0.01)
        self.filter_logics()

    def get_logic(self, eth):
        for log in self.logics:
            if log.con and log.con.passes(eth):
                return log
        if not any(map(lambda x: x[0].passes(eth), self.remcon)):
            con = Connection(eth, self.server_ips)
            proc = DefaultQueueControl(con.qi, con.qo)
            proc.start()
            log = LogicElement(None, con, proc, con.qi, con.qo)
            self.logics.add(log)
            return log

    def con_logic(self, curlog, eth):
        if curlog.con.state in (Connection.STABLE, Connection.WAIT):
            if curlog.con.state == Connection.WAIT:
                self.qo.put(eth)
            curlog.con.update(eth)
            apply(self.qo.put, curlog.con.idle())

    def check_logon(self, curlog, eth):
        ip, tcp, data = unstack(eth)
        if data and ip.header.destination in self.server_ips and data[0] == 0x68:
            char_name = str(c2s_packets.parse(data).char_name, encoding="ascii")
            remlog = set()
            for log in self.logics:
                if log.name == char_name:
                    log.con = curlog.con
                    log.con.qi = log.qi
                    log.con.qo = log.qo
                    curlog.logic.terminate()
                    remlog.add(curlog)
                    curlog = log
                    break
            else:
                curlog.name = char_name
            self.logics = self.logics - remlog
        return curlog

    def run(self):
        while True:
            self.idle()
            eth = self.qi.get()
            curlog = self.get_logic(eth)
            if curlog:
                if not curlog.name:
                    curlog = self.check_logon(curlog, eth)
                self.con_logic(curlog, eth)
