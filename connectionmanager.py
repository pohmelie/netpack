from multiprocessing import Process, Queue, log_to_stderr
import logging
from plugin import PluginManager

logger = log_to_stderr()
logger.setLevel(logging.WARNING)


class LogicElement():
    def __init__(self, name=None, con=None, logic=None):
        self.name = name
        self.con = con
        self.logic = logic

class ConnectionManager(Process):
    def __init__(self, qi, qo, server_ips):
        Process.__init__(self)

        self.qi = qi
        self.qo = qo
        self.server_ips = server_ips

        self.connections = ()
        self.logics = {}

    def run(self):
        self.plugman = PluginManager()
        while True:
            self.qo.put(self.qi.get())

