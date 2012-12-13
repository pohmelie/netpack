from construct import *
from d2packetparser_c2s import c2s_packets
from d2packetparser_s2c import s2c_packets


d2_packet_parser = (OptionalGreedyRange(c2s_packets), OptionalGreedyRange(s2c_packets))


from d2crypt import decrypt
from connection import unstack, Connection
from time import time

def tmp(eth, ips):
    ip, tcp, data = unstack(eth)
    if not data:
        return
    if ip.header.source in ips:
        try:
            data = decrypt(data)
        except:
            pass
        s = Connection.SERVER
    else:
        s = Connection.CLIENT

    try:
        x = d2_packet_parser[s].parse(data)
    except:
        print("\nError when parsing:")
        print(data)

    pphex = lambda data: " ".join(map("{:0>2x}".format, data))
    #print(pphex(data))


    if d2_packet_parser[s].build(x) != data or x[-1].fun == "unknown":
        print("=====================================================================")
        if s == Connection.SERVER:
            print("[{:.3f}] s -> c:".format(time() % 60))
        else:
            print("[{:.3f}] c -> s:".format(time() % 60))
        print(pphex(data))
        print(pphex(d2_packet_parser[s].build(x)))
        print(x)
    elif s == Connection.SERVER:
        for p in x:
            if p.fun in ("world_item_action", "owner_item_action"):
                print("\n\nitem packet:")
                print(p)
