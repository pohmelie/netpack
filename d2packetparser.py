from construct import *
from d2packetparser_c2s import parse_c2s


d2_packet_parser = (GreedyRange(c2s_packets), GreedyRange(s2c_packets))
