from construct import *
from d2packetparser_c2s import c2s_packets
from d2packetparser_s2c import s2c_packets


d2_packet_parser = (OptionalGreedyRange(c2s_packets), OptionalGreedyRange(s2c_packets))


from d2crypt import Decrypter
from connection import unstack, Connection
from time import time
from recipe import *

dec = Decrypter()

from multiprocessing import log_to_stderr, SUBDEBUG
import logging
logger = log_to_stderr()
logger.setLevel(logging.WARNING)

def tmp(data, s, d):
    if not data:
        return
    #logger.warning("")
    #logger.warning(rev(data))
    ddata = (data,)
    if data != b"\xaf\x01" and s == Connection.SERVER:
        ddata = dec.decrypt(data)

    #logger.warning("head = " + rev(dec.head))
    #logger.warning("decrypted count = {}".format(len(ddata)))
    for dat in ddata:
        #logger.warning("\ndecrypted = " + rev(dat))
        x = d2_packet_parser[s].parse(dat)
        #logger.warning(x)
        if x and (d2_packet_parser[s].build(x) != dat or x[-1].fun == "unknown"):
            logger.warning("=====================================================================")
            if s == Connection.SERVER:
                logger.warning("[{:.3f}] s -> c:".format(time() % 60))
            else:
                logger.warning("[{:.3f}] c -> s:".format(time() % 60))
            logger.warning(rev(d2_packet_parser[s].build(x)))
            logger.warning(x)
        elif s == Connection.SERVER:
            for p in x:
                if p.fun in ("world_item_action", "owner_item_action"):
                    logger.warning(p)
        elif s == Connection.CLIENT:
            for p in x:
                if p.fun in ("run", "walk"):
                    logger.warning(p)
