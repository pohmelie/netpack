from construct import *


s2c_packets = Struct("s2c packets",
    UBInt8("fun")
)

d2_packet_parser = (GreedyRange(c2s_packets), GreedyRange(s2c_packets))
