from ipstack import layer3_ipv4
from construct.protocols.layer4.tcp import tcp_header


def recalculateIPchecksum(ip):
    ip.header.checksum = 0
    ipbin = layer3_ipv4.build(ip)
    step = lambda i: (ipbin[i] << 8) + ipbin[i + 1]
    cs = sum(map(step , range(0, ip.header.header_length, 2)))
    while cs >> 16:
        cs = (cs & 0xffff) + (cs >> 16)
    ip.header.checksum = cs ^ 0xffff

def recalculateTCPchecksum(ip):
    tcp = ip.next
    tcp.header.checksum = 0
    tcpbin = tcp_header.build(tcp.header) + tcp.next + bytes((0,))
    tcplength = ip.header.total_length - ip.header.header_length
    step = lambda i: (tcpbin[i] << 8) + tcpbin[i + 1]
    cs = sum(map(step , range(0, ((tcplength + 1) >> 1) << 1, 2)))
    ip2num = lambda x: tuple(map(int, x.split(".")))
    ip2cs = lambda x: ((x[0] + x[2]) << 8) + x[1] + x[3]
    cs = cs + sum(map(ip2cs, map(ip2num, (ip.header.source, ip.header.destination))))
    IPPROTO_TCP = 6
    cs = cs + IPPROTO_TCP + (tcplength & 0xffff)
    while cs >> 16:
        cs = (cs & 0xffff) + (cs >> 16)
    tcp.header.checksum = cs ^ 0xffff

def recalculatechecksums(ip):
    recalculateIPchecksum(ip)
    recalculateTCPchecksum(ip)
