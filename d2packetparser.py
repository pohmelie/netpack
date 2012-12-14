from construct import *
from d2packetparser_c2s import c2s_packets
from d2packetparser_s2c import s2c_packets


d2_packet_parser = (OptionalGreedyRange(c2s_packets), OptionalGreedyRange(s2c_packets))


from d2crypt import Decrypter
from connection import unstack, Connection
from time import time
from recipe import *

d = Decrypter()

def tmp(eth, ips):
    ip, tcp, data = unstack(eth)
    if not data:
        return
    print()
    print(rev(data))
    ddata = (data,)
    if ip.header.source in ips:
        if data != b"\xaf\x01":
            ddata = d.decrypt(data)
        s = Connection.SERVER
    else:
        s = Connection.CLIENT

    print("head =", rev(d.head))
    print("decrypted count =", len(ddata))
    for dat in ddata:
        print("\ndecrypted =", rev(dat))
        x = d2_packet_parser[s].parse(dat)
        print(x)
        if x and (d2_packet_parser[s].build(x) != dat or x[-1].fun == "unknown"):
            print("=====================================================================")
            if s == Connection.SERVER:
                print("[{:.3f}] s -> c:".format(time() % 60))
            else:
                print("[{:.3f}] c -> s:".format(time() % 60))
            print(rev(d2_packet_parser[s].build(x)))
            print(x)
        elif s == Connection.SERVER:
            for p in x:
                if p.fun in ("world_item_action", "owner_item_action"):
                    continue
                    print("\n\nitem packet:")
                    print(p)
