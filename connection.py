from construct.lib.container import Container
from time import time
from copy import deepcopy
from multiprocessing import Queue

from checksum import *
from recipe import *


unstack = lambda eth: (eth.next, eth.next.next, eth.next.next.next)
_add = lambda x, y: (x + y) % (1 << 32)

def pp(eth):
    ip, tcp, data = unstack(eth)
    print("[{:.3f}]".format(time() % 60), ip.header.source, "->", ip.header.destination)
    print(tcp.header.seq, tcp.header.ack, len(data))

def seqgt(x, y):#x > y
    if abs(x - y) > (1 << 31):
        return x < y
    else:
        return x > y

class PacketInfo():
    RESEND, WAIT, TIMEOUT = tuple(range(3))
    def __init__(self, eth, delay=0.5, repeat=3):
        self.eth = deepcopy(eth)
        self.delay = delay
        self.repeat = repeat
        _, tcp, data = unstack(eth)
        self.seq = tcp.header.seq
        self.ack = tcp.header.ack
        self.ldata = len(data)
        self.time = time()

    def resend(self):
        t = time()
        if t - self.time > self.delay:
            if self.repeat != 0:
                self.time = t
                self.repeat = self.repeat - 1
                return PacketInfo.RESEND
            return PacketInfo.TIMEOUT
        return PacketInfo.WAIT

class ConnectionOutputQueue():
    def __init__(self):
        self.p = ()
        self.ack = None
        self.seq = None

    def update(self, seq, ack):
        self.ack = seq
        self.p = tuple(filter(lambda p: seqgt(_add(p.seq, p.ldata), ack), self.p))

    def add(self, eth):
        ip, tcp, data = unstack(eth)

        if tcp.header.flags.syn:
            self.seq = tcp.header.seq + 1
        else:
            if self.seq == None:
                self.seq = tcp.header.seq
            tcp.header.seq = self.seq

        if self.ack != None and not (tcp.header.ack == 0 and tcp.header.flags.syn):
            tcp.header.ack = self.ack

        self.seq = _add(self.seq, len(data))
        recalculatechecksums(ip)
        if len(data) != 0:
            self.p = self.p + (PacketInfo(eth),)
        return eth

    def resend(self):
        ret = ()
        for p in self.p:
            rcode = p.resend()
            if rcode == PacketInfo.RESEND:
                ret = ret + (p.eth,)
            elif rcode == PacketInfo.TIMEOUT:
                return PacketInfo.TIMEOUT
        return ret

class ConnectionInputQueue():
    def __init__(self):
        self.p = {}
        self.seq = None

    def add(self, eth):
        _, tcp, data = unstack(eth)
        if self.seq == None or tcp.header.flags.syn:
            self.seq = _add(tcp.header.seq, len(data) + (1 if tcp.header.flags.syn else 0))
            return (eth,)
        elif seqgt(self.seq, tcp.header.seq):
            return ()
        elif self.seq == tcp.header.seq:
            ret = (eth,)
            self.seq = _add(self.seq, len(data))
            while self.seq in self.p:
                e = self.p.pop(self.seq)
                ret = ret + (e,)
                _, _, d = unstack(e)
                self.seq = _add(self.seq, len(d))
            return ret
        else:
            self.p[tcp.header.seq] = deepcopy(eth)
            return ()

class Connection():
    CLIENT, SERVER = tuple(range(2))
    TIMEOUT, STABLE, RESET, WAIT = tuple(range(4))
    def __init__(self, eth, server_ips, qi=None, qo=None):
        self.i = (ConnectionInputQueue(), ConnectionInputQueue())
        self.o = (ConnectionOutputQueue(), ConnectionOutputQueue())
        self.qi = qi or Queue()
        self.qo = qo or Queue()
        self.state = Connection.WAIT
        self.reset = [False, False]

        ip, tcp, data = unstack(eth)
        if ip.header.source in server_ips:
            self.mac = (eth.header.destination, eth.header.source)
            self.ip = (ip.header.destination, ip.header.source)
            self.port = (tcp.header.destination, tcp.header.source)
        else:
            self.mac = (eth.header.source, eth.header.destination)
            self.ip = (ip.header.source, ip.header.destination)
            self.port = (tcp.header.source, tcp.header.destination)

    def direction(self, eth):
        if eth.next.header.source == self.ip[0]:
            return (Connection.CLIENT, Connection.SERVER)
        else:
            return (Connection.SERVER, Connection.CLIENT)

    def passes(self, eth):
        ip, tcp, data = unstack(eth)
        ip = (ip.header.source, ip.header.destination)
        port = (tcp.header.source, tcp.header.destination)
        return (port, ip) in ((self.port, self.ip), (self.port[::-1], self.ip[::-1]))

    def idle(self):
        ret = ()
        while not self.qo.empty():
            data, s , d = self.qo.get()
            if data == Connection.RESET:
                ret = ret + (self.o[d].add(self.make(b"", s == Connection.CLIENT, True)),)
            elif not self.reset[d]:
                ret = ret + (self.o[d].add(self.make(data, s == Connection.CLIENT)),)

        rss, rsc = self.o[Connection.SERVER].resend(), self.o[Connection.CLIENT].resend()
        if (rsc == None or rss == None) and self.state != Connection.RESET:
            self.state = Connection.TIMEOUT

        return ret + (rss or ()) + (rsc or ())

    def update(self, eth):
        ip, tcp, data = unstack(eth)
        s, d = self.direction(eth)

        checksum = tcp.header.checksum
        recalculatechecksums(ip)
        if checksum != tcp.header.checksum or self.reset[s]:
            return

        if tcp.header.flags.rst:
            self.reset[s] = True
            self.qo.put((Connection.RESET, s, d))
            if all(self.reset):
                self.state = Connection.RESET
            return

        if self.state != Connection.WAIT:
            eths = self.i[s].add(eth)
            self.o[s].update(self.i[s].seq, tcp.header.ack)
            self.qo.put((b"", d, s))
            self.qo.put((b"", s, d))
            for _, _, dat in map(unstack, eths):
                if len(dat) != 0 and not any(self.reset):
                    self.qi.put((dat, s, d))
        else:
            self.i[s].add(eth)
            self.o[s].update(self.i[s].seq, tcp.header.ack)
            self.o[d].add(eth)
            if self.i[s].seq and self.i[d].seq:
                self.state = Connection.STABLE

    def make(self, data, c2s, reset=False):
        if c2s:
            s, d = (Connection.CLIENT, Connection.SERVER)
        else:
            s, d = (Connection.SERVER, Connection.CLIENT)

        _eth.header.source = self.mac[s]
        _eth.header.destination = self.mac[d]

        ip = _eth.next
        tcp = ip.next

        ip.header.source = self.ip[s]
        ip.header.destination = self.ip[d]
        ip.header.payload_length = ip.header.header_length + len(data)
        ip.header.total_length = ip.header.payload_length + tcp.header.header_length

        tcp.header.source = self.port[s]
        tcp.header.destination = self.port[d]
        tcp.header.flags.psh = len(data) != 0
        tcp.header.flags.rst = reset
        tcp.next = data

        recalculatechecksums(ip)
        return deepcopy(_eth)

_eth = Container(
        header = Container(
            source = '00-00-00-00-00-00',
            destination = '00-00-00-00-00-00',
            type = 'IPv4'),
        next = Container(
            header = Container(
                header_length = 20,
                protocol = 'TCP',
                payload_length = 20,
                tos = Container(
                    minimize_cost = False,
                    high_throuput = False,
                    minimize_delay = False,
                    precedence = 0,
                    high_reliability = False),
                frame_offset = 0,
                flags = Container(
                    dont_fragment = True,
                    more_fragments = False),
                source = '0.0.0.0',
                destination = '0.0.0.0',
                version = 4,
                identification = 32768,
                ttl = 128,
                total_length = 40,
                checksum = 0,
                options = b''),
                next = Container(
                    header = Container(
                        header_length = 20,
                        seq = 0,
                        urgent = 0,
                        ack = 0,
                        checksum = 0,
                        destination = 0,
                        source = 0,
                        window = 32768,
                        flags = Container(
                            ece = False,
                            urg = False,
                            ack = True,
                            cwr = False,
                            psh = True,
                            syn = False,
                            rst = False,
                            ns = False,
                            fin = False),
                        options = b''),
                        next = b'')))
