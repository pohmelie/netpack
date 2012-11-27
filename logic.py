from connection import *
from time import time

from winpkbind import phex


class Logic():
    READY = tuple(range(1))
    ID = 0
    def __init__(self):
        self.lid = Logic.ID
        Logic.ID = Logic.ID + 1
        self.runs = 0
        self.state = Logic.READY

    @staticmethod
    def iscommand(data):
        return data[0] == 0x15 and str(data[3:4], "ascii") == "\\"

    @staticmethod
    def getcommand(data):
        return str(data[3: -3], "ascii")

    def callback(self, data, s, d):
        print("\n[{:.3f} s.] lid = {}".format(time() % 60, self.lid))
        print(phex(data))
        print(data)

        if s == Connection.CLIENT and Logic.iscommand(data):
            command = Logic.getcommand(data).lower()
            if command == "\\exit":
                exit(0)
            elif command == "\\help":
                #sending info to client
                pass

        return False, ((), ())
