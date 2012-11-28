from ctypes import *
from winpkbind import *
from ipstack import ip_stack
from connection import *
from logic import *
from time import time
from functools import partial


class Netpack():
    def __init__(self, server_ips, adapter_id=None):
        self.server_ips = server_ips
        self.logics = ()
        self.connections = ()

        self.ndisapi = windll.ndisapi
        self.kernel32 = windll.kernel32

        self.hnd = self.ndisapi.OpenFilterDriver(DRIVER_NAME_A)
        tmp = TCP_AdapterList()
        self.ndisapi.GetTcpipBoundAdaptersInfo(self.hnd, byref(tmp))

        self.mode = ADAPTER_MODE()
        self.mode.dwFlags = MSTCP_FLAG_SENT_TUNNEL | MSTCP_FLAG_RECV_TUNNEL
        if adapter_id == None:
            print("Use 'ipconfig /all' to determine your mac address")
            for i in range(tmp.m_nAdapterCount):
                print("{}). {}".format(i + 1, pmac(tmp.m_czCurrentAddress[i])))
            adapter_id = int(input("#: "))
        self.mode.hAdapterHandle = tmp.m_nAdapterHandle[adapter_id - 1]

        self.hEvent = self.kernel32.CreateEventW(None, True, False, None)
        self.ndisapi.SetPacketEvent(self.hnd, self.mode.hAdapterHandle, self.hEvent)

        self.request = ETH_REQUEST()
        self.packetbuffer= INTERMEDIATE_BUFFER()

        self.request.EthPacket.Buffer = pointer(self.packetbuffer)
        self.request.hAdapterHandle = self.mode.hAdapterHandle

        self.ndisapi.SetAdapterMode(self.hnd, byref(self.mode))

    def __enter__(self):
        return self

    def __exit__(self, t, value, traceback):
        self.release()

    def release(self):
        self.mode.dwFlags = 0
        self.ndisapi.SetPacketEvent(self.hnd, self.mode.hAdapterHandle, None)
        self.kernel32.CloseHandle(self.hEvent)
        self.ndisapi.SetAdapterMode(self.hnd, byref(self.mode))
        self.ndisapi.FlushAdapterPacketQueue(self.hnd, self.mode.hAdapterHandle)

    def make_request(self, raw, m_dwDeviceFlags):
        _request = ETH_REQUEST()
        _packetbuffer= INTERMEDIATE_BUFFER()

        _request.EthPacket.Buffer = pointer(_packetbuffer)
        _request.hAdapterHandle = self.mode.hAdapterHandle
        _packetbuffer.m_dwDeviceFlags = m_dwDeviceFlags
        _packetbuffer.m_Flags = 130

        _packetbuffer.m_Length = len(raw)
        for i in range(_packetbuffer.m_Length):
            _packetbuffer.m_IBuffer[i] = raw[i]
        return _request

    def checkfortcp(self, t):#ipv4 & tcp protocols
        return t[12:14] == b"\x08\x00" and t[14 + 9] == 6

    def checkforips(self, t):
        eth = ip_stack.parse(t)
        ip, tcp, data = unstack(eth)
        return ip.header.destination in self.server_ips or ip.header.source in self.server_ips

    def send(self, request):
        if request.EthPacket.Buffer.contents.m_dwDeviceFlags == PACKET_FLAG_ON_SEND:
            self.ndisapi.SendPacketToAdapter(self.hnd, byref(request))
        else:
            self.ndisapi.SendPacketToMstcp(self.hnd, byref(request))

    def sendpacks(self, packs):
        for eth in packs[0]:
            r = ip_stack.build(eth)
            self.send(self.make_request(r, PACKET_FLAG_ON_SEND))
        for eth in packs[1]:
            r = ip_stack.build(eth)
            self.send(self.make_request(r, PACKET_FLAG_ON_RECEIVE))

    def defaultlogic(self, con, data, s, d):
        if s == Connection.CLIENT and Logic.iscommand(data):
            command = Logic.getcommand(data).lower()
            if command == "\\init":
                logic = Logic()
                con.callback = logic.callback
                self.logics = self.logics + (logic,)
            elif command.startswith("\\bot"):
                try:
                    w, n = tuple(command.split())
                    for logic in self.logics:
                        if logic.lid == int(n) - 1:
                            con.callback = logic.callback
                            break
                except:
                    pass
            return True, ((), (b"",))
        else:
            return False, ((), ())

    def mainloop(self):
        while True:
            self.kernel32.WaitForSingleObject(self.hEvent, 100)
            x = c_ulong()
            self.ndisapi.GetAdapterPacketQueueSize(self.hnd, self.mode.hAdapterHandle, byref(x))
            if x.value == 0:
                for con in self.connections:
                    packs = (con.o[Connection.SERVER].resend(), con.o[Connection.CLIENT].resend())
                    self.sendpacks(packs)
            else:
                while self.ndisapi.ReadPacket(self.hnd, byref(self.request)):
                    d = bytes(self.packetbuffer.m_IBuffer[:self.packetbuffer.m_Length])
                    if self.checkfortcp(d) and self.checkforips(d):
                        eth = ip_stack.parse(d)
                        ip, tcp, data = unstack(eth)
                        active_con = None
                        for con in self.connections:
                            if con.passes(eth):
                                retcode, packs = con.update(eth)
                                active_con = con
                                break
                        if active_con == None and not tcp.header.flags.rst:
                            active_con = Connection(eth, self.server_ips)
                            deflog = partial(self.defaultlogic, active_con)
                            active_con.callback = deflog
                            self.connections = self.connections + (active_con,)
                            retcode, packs = active_con.update(eth)

                        if active_con:
                            if retcode == Connection.TIMEOUT or retcode == Connection.RESET:
                                self.connections = tuple(filter(
                                    lambda x: x is not active_con,
                                    self.connections))
                            self.sendpacks(packs)
                    else:
                        self.send(self.request)
            self.kernel32.ResetEvent(self.hEvent)

if __name__ == "__main__":
    ips = tuple(map(lambda x: x.strip(), open("ip.txt")))
    with Netpack(ips, 2) as npack:
        print("netpack 2012.11.27\n\ntype '\init' in game for more information\nuse ctrl-c to exit\n")
        npack.mainloop()
