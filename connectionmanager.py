from multiprocessing import Process, Queue, log_to_stderr
import logging
from plugin import PluginManager
from connection import Connection
from recipe import *

logger = log_to_stderr()
logger.setLevel(logging.WARNING)


class LogicElement():
    def __init__(self, name=None, con=None, logic=None):
        self.name = name
        self.con = con
        self.logic = logic

    def smth(self, val):
        return name == val or con == val or logic == val

class ConnectionManager(Process):
    def __init__(self, qi, qo, server_ips):
        Process.__init__(self)

        self.qi = qi
        self.qo = qo
        self.server_ips = server_ips

        self.logics = ()

    @staticmethod
    def default_queue_control(qi, qo):
        while True:
            qo.put(qi.get())

    def run(self):
        self.plugman = PluginManager()
        while True:
            #idle
            while self.qi.empty():
                for log in self.logics:
                    apply(self.qo.put, log.con.idle())
                    if log.con.state == Connection.TIMEOUT:
                        pass
                        #delete connection and 'None' it in logics
            #active
            eth = self.qi.get()
            for log in self.logics:
                if log.con.passes(eth):
                    curcon = log.con
                    break
            else:
                curcon = Connection(eth, server_ips)
                proc = Process(
                    target=ConnectionManager.default_queue_control,
                    args=(curcon.qi, curcon.qo))
                log = LogicElement(None, curcon, proc)
                connections = connections + curcon
            self.qo.put(self.qi.get())

