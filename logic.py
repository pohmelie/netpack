from connection import *
from time import time
from d2crypt import decrypt
from d2packet import PacketSplitter

from winpkbind import phex


packetsplitter = PacketSplitter()

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
        '''print("\n[{:.3f} s.] lid = {}".format(time() % 60, self.lid))
        print(phex(data))
        print(data)'''

        if s == Connection.SERVER:
            data = decrypt(data)
            packs = packetsplitter.split(data, s)
            for pack in packs:
                if pack[0] == 0x51:
                    p = packetsplitter.funcs[s][pack[0]].unpack(pack)
                    if p["Object Code"] == 160:
                        print("Fire at [{}, {}]".format(p["x"], p["y"]))
                elif pack[0] == 0x15:
                    p = packetsplitter.funcs[s][pack[0]].unpack(pack)
                    if p["Unit Id"] == 1:
                        print("[{}, {}]".format(p["x"], p["y"]))
                elif pack[0] == 0x07:
                    p = packetsplitter.funcs[s][pack[0]].unpack(pack)
                    print("[{:.3f}] Map Reveal [{}, {}] [{}]".format(
                        time() % 60,
                        p["Tile X"] >> 3,
                        p["Tile Y"] >> 3,
                        p["Area Id"])
                    )

        if s == Connection.CLIENT and Logic.iscommand(data):
            command = Logic.getcommand(data).lower()
            if command == "\\exit":
                exit(0)
            elif command == "\\help":
                #sending info to client
                pass
            elif command.startswith("\\tp"):
                x, y = tuple(map(int, command.split()[1:]))
                print("Trying to teleport to [{}, {}]".format(x, y))
                print(b"\x0c" + bytes((x & 0xff, x >> 8, y & 0xff, y >> 8)))
                return True, ((b"\x0c" + bytes((x & 0xff, x >> 8, y & 0xff, y >> 8)),), ())

        return False, ((), ())
