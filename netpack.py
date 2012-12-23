from ctypes import *
from winpkbind import *
from ipstack import ip_stack
from multiprocessing import Queue
from connectionmanager import ConnectionManager
from atexit import register


class Netpack():
    def __init__(self, server_ips, mac=None):
        self.server_ips = server_ips
        raw_ips = lambda ip: bytes(map(int, ip.split(".")))
        self.server_ips_raw = tuple(map(raw_ips, server_ips))

        self.qi = Queue()
        self.qo = Queue()
        ConnectionManager(self.qi, self.qo, server_ips).start()

        self.ndisapi = windll.ndisapi
        self.kernel32 = windll.kernel32

        self.hnd = self.ndisapi.OpenFilterDriver(DRIVER_NAME_A)
        tmp = TCP_AdapterList()
        self.ndisapi.GetTcpipBoundAdaptersInfo(self.hnd, byref(tmp))

        self.mode = ADAPTER_MODE()
        self.mode.dwFlags = MSTCP_FLAG_SENT_TUNNEL | MSTCP_FLAG_RECV_TUNNEL

        adapter_id = None
        if mac != None:
            for i in range(tmp.m_nAdapterCount):
                if mac == pmac(tmp.m_czCurrentAddress[i]):
                    adapter_id = i + 1
                    break
            else:
                print("Can't find mac = {} in adapters list\n".format(mac))
        if adapter_id == None:
            print("Use 'ipconfig /all' to determine your mac address")
            print("you can write it in 'mac.txt' for more silent run\n")
            for i in range(tmp.m_nAdapterCount):
                print("{}). {}".format(i + 1, pmac(tmp.m_czCurrentAddress[i])))
            adapter_id = int(input("#: "))
            mac = pmac(tmp.m_czCurrentAddress[adapter_id - 1])

        print("\nUsing:\n\tadapter id = {}\n\tmac = {}".format(adapter_id, mac))
        self.mode.hAdapterHandle = tmp.m_nAdapterHandle[adapter_id - 1]

        self.hEvent = self.kernel32.CreateEventW(None, True, False, None)
        self.ndisapi.SetPacketEvent(self.hnd, self.mode.hAdapterHandle, self.hEvent)

        self.request = ETH_REQUEST()
        self.packetbuffer= INTERMEDIATE_BUFFER()
        self.request.EthPacket.Buffer = pointer(self.packetbuffer)
        self.request.hAdapterHandle = self.mode.hAdapterHandle

        self.ndisapi.SetAdapterMode(self.hnd, byref(self.mode))
        register(self.release)

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
        s, d = t[14 + 12:14 + 16], t[14 + 16:14 + 20]
        return s in self.server_ips_raw or d in self.server_ips_raw

    def send(self, request):
        if request.EthPacket.Buffer.contents.m_dwDeviceFlags == PACKET_FLAG_ON_SEND:
            self.ndisapi.SendPacketToAdapter(self.hnd, byref(request))
        else:
            self.ndisapi.SendPacketToMstcp(self.hnd, byref(request))

    def sendpack(self, eth):
        ip = eth.next
        if ip.header.source in self.server_ips:
            flag = PACKET_FLAG_ON_RECEIVE
        else:
            flag = PACKET_FLAG_ON_SEND
        self.send(self.make_request(ip_stack.build(eth), flag))

    def mainloop(self):
        while True:
            self.kernel32.WaitForSingleObject(self.hEvent, 10)
            while self.ndisapi.ReadPacket(self.hnd, byref(self.request)):
                d = bytes(self.packetbuffer.m_IBuffer[:self.packetbuffer.m_Length])
                if self.checkfortcp(d) and self.checkforips(d):
                    self.qi.put_nowait(ip_stack.parse(d))
                else:
                    self.send(self.request)

            while not self.qo.empty():
                self.sendpack(self.qo.get())
            self.kernel32.ResetEvent(self.hEvent)

if __name__ == "__main__":
    print("netpack 2012.12.24")
    mac = None
    for line in open("mac.txt"):
        if line[0] != "#":
            mac = line.strip()
            break
    Netpack(tuple(map(lambda x: x.strip(), open("ip.txt"))), mac).mainloop()
