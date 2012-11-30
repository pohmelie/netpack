from itertools import takewhile


pp_packet = lambda packet: " ".join(map(lambda x: "{:0>2x}".format(x), packet))

class PacketFunc():
    def __init__(self, func, size, info):
        self.counters = {"b":1, "h":2, "i":4}
        self.func = func
        self.size = size
        self.desc = info[0]
        if len(info) > 1:
            self.fmt = info[1]
            self.args = info[2:]

    def unpack(self, packet):
        ret, counter, index, num, s = [], 0, 1, 0, ""
        for ch in self.fmt:
            if ch.isdigit():
                counter = counter * 10 + int(ch)
            elif ch.lower() in self.counters:
                for _ in range(1 if not counter else counter):
                    for i in range(self.counters[ch.lower()]):
                        num += packet[index] << (i * 8)
                        index += 1
                    ret.append(num)
                    num = 0
                counter = 0
            elif ch.lower() == "s":
                if not counter:
                    while packet[index]:
                        s += chr(packet[index])
                        index += 1
                    index += 1
                    ret.append(s)
                    s = str()
                else:
                    ret.append(packet[index:index + counter])
                    index += counter
                    s, counter = str(), 0
            elif ch.lower() == "x":
                index += 1 if not counter else counter
                counter = 0
        return dict(zip(self.args, ret))

def chat_s2c_0x26(p):
    if p[1] == 0x05 and p[2] == 0 and p[3] == 0:
        return 13 + sum(1 for _ in takewhile(bool, p[12:]))
    else:
        index = 10
        while p[index]:
            index += 1
        index += 1
        while p[index]:
            index += 1
        return index + 1

packet_size = (
    {
        0x14:lambda p: 6 + sum(1 for _ in takewhile(bool, p[3:])),
        0x15:lambda p: 6 + sum(1 for _ in takewhile(bool, p[3:])),
        0x66:lambda p: 3 + p[1]
    },
    {
        0x26:chat_s2c_0x26,
        0x94:lambda p: 6 + p[1] * 3,
        0x9c:lambda p: p[2],
        0x9d:lambda p: p[2],
        0xa8:lambda p: p[6],
        0xaa:lambda p: p[6],
        0xac:lambda p: p[12]
    }
)

class PacketSplitter():
    def __init__(self, c2s_fname="c2s.txt", s2c_fname="s2c.txt"):
        self.funcs = ({}, {})
        for c, cfname in zip(self.funcs, (c2s_fname, s2c_fname)):
            c.clear()
            cf = open(cfname)
            for line in cf:
                elements = line.strip().split("|")
                func = int(elements[0], 16)
                size = int(elements[1]) if elements[1] != "*" else 0
                c[func] = PacketFunc(func, size, elements[2:])
            cf.close()

    def split(self, packet, s):
        ret = ()
        while packet:
            func = packet[0]
            if func in self.funcs[s]:
                size = self.funcs[s][func].size
                if size == 0:
                    size = packet_size[s][func](packet)
                ret = ret + (packet[:size],)
                packet = packet[size:]
            else:
                ret = ret + (packet,)
                packet = None
        return ret
