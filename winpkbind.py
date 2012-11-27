from ctypes import *


#constants
NDISRD_VERSION = 0x00073000

DRIVER_NAME_A = b"NDISRD"
DRIVER_NAME_U = "NDISRD"
DEVICE_NAME = "\\Device\\NDISRD"
SYMLINK_NAME = "\\DosDevices\\NDISRD"
WIN9X_REG_PARAM = "System\\CurrentControlSet\\Services\\VxD\\ndisrd\\Parameters"
WINNT_REG_PARAM = "SYSTEM\\CurrentControlSet\\Services\\ndisrd\\Parameters"

FILTER_FRIENDLY_NAME = "WinpkFilter NDIS LightWeight Filter"
FILTER_UNIQUE_NAME = "{5cbf81bd-5055-47cd-9055-a76b2b4e3697}"
FILTER_SERVICE_NAME = "NDISRD"

ADAPTER_NAME_SIZE = 256
ADAPTER_LIST_SIZE = 32
ETHER_ADDR_LENGTH = 6
MAX_ETHER_FRAME = 65535

MSTCP_FLAG_SENT_TUNNEL = 0x00000001
MSTCP_FLAG_RECV_TUNNEL = 0x00000002
MSTCP_FLAG_SENT_LISTEN = 0x00000004
MSTCP_FLAG_RECV_LISTEN = 0x00000008
MSTCP_FLAG_FILTER_DIRECT = 0x00000010
MSTCP_FLAG_LOOPBACK_FILTER = 0x00000020
MSTCP_FLAG_LOOPBACK_BLOCK = 0x00000040

PACKET_FLAG_ON_SEND = 0x00000001
PACKET_FLAG_ON_RECEIVE = 0x00000002

ANY_SIZE = 1

RAS_LINK_BUFFER_LENGTH = 1024
RAS_LINKS_MAX = 256


#functions
bytes2str = lambda x: "".join(map(chr, filter(bool, x)))
pmac = lambda x: ":".join(map(lambda x: "{:0>2X}".format(x), x))
phex = lambda x, cnt=None: " ".join(map(lambda x: "{:0>2X}".format(x), x[:cnt]))
peth = lambda x: ".".join(map(str, x[2:]))


#structures
class ADAPTER_EVENT(Structure):
    _fields_ = [
        ("hAdapterHandle", c_void_p),
        ("hEvent", c_void_p)
    ]

class ADAPTER_MODE(Structure):
    _fields_ = [
        ("hAdapterHandle", c_void_p),
        ("dwFlags", c_ulong)
    ]

class ETH_802_3_FILTER(Structure):
    _fields_ = [
        ("m_ValidFields", c_ulong),
        ("m_SrcAddress", c_ubyte * ETHER_ADDR_LENGTH),
        ("m_DestAddress", c_ubyte * ETHER_ADDR_LENGTH),
        ("m_Protocol", c_ushort)
    ]

class DATA_LINK_LAYER_FILTER(Structure):
    _fields_ = [
        ("m_dwUnionSelector", c_ulong),
        ("m_Eth8023Filter", ETH_802_3_FILTER)
    ]

class LIST_ENTRY(Structure):
    pass

LIST_ENTRY._fields_ = [
        ("Flink", POINTER(LIST_ENTRY)),
        ("Blink", POINTER(LIST_ENTRY))
    ]

class INTERMEDIATE_BUFFER(Structure):
    _fields_ = [
        ("m_qLink", LIST_ENTRY),
        ("m_dwDeviceFlags", c_ulong),
        ("m_Length", c_ulong),
        ("m_Flags", c_ulong),
        ("m_IBuffer", c_ubyte * MAX_ETHER_FRAME)
    ]

class NDISRD_ETH_Packet(Structure):
    _fields_ = [
        ("Buffer", POINTER(INTERMEDIATE_BUFFER))
    ]

class ETH_M_REQUEST(Structure):
    _fields_ = [
        ("hAdapterHandle", c_void_p),
        ("dwPacketsNumber", c_uint),
        ("dwPacketsSuccess", c_uint),
        ("EthPacket", NDISRD_ETH_Packet * ANY_SIZE)
    ]

class ETH_REQUEST(Structure):
    _fields_ = [
        ("hAdapterHandle", c_void_p),
        ("EthPacket", NDISRD_ETH_Packet)
    ]

class IP_RANGE_V4(Structure):
    _fields_ = [
        ("m_StartIp", c_ulong),
        ("m_EndIp", c_ulong)
    ]

class IP_SUBNET_V4(Structure):
    _fields_ = [
        ("m_Ip", c_ulong),
        ("m_IpMask", c_ulong)
    ]

class Ipv4AddressType(Union):
    _fields_ = [
        ("m_IpSubnet", IP_SUBNET_V4),
        ("m_IpRange", IP_RANGE_V4)
    ]

class IP_ADDRESS_V4(Structure):
    _fields_ = [
        ("m_AddressType", c_ulong),
        ("u", Ipv4AddressType)
    ]

class IP_V4_FILTER(Structure):
    _fields_ = [
        ("m_ValidFields", c_ulong),
        ("m_SrcAddress", IP_ADDRESS_V4),
        ("m_DestAddress", IP_ADDRESS_V4),
        ("m_Protocol", c_ubyte)
    ]

class NETWORK_LAYER(Union):
    _fields_ = [
        ("m_IPv4", IP_V4_FILTER)
    ]

class NETWORK_LAYER_FILTER(Structure):
    _fields_ = [
        ("m_dwUnionSelector", c_ulong),
        ("u", NETWORK_LAYER)
    ]

class PACKET_OID_DATA(Structure):
    _fields_ = [
        ("hAdapterHandle", c_void_p),
        ("Oid", c_ulong),
        ("Length", c_ulong),
        ("Data", c_ubyte * 1)
    ]

class PORT_RANGE(Structure):
    _fields_ = [
        ("m_StartRange", c_ushort),
        ("m_EndRange", c_ushort)
    ]

class RAS_LINK_INFO(Structure):
    _fields_ = [
        ("LinkSpeed", c_ulong),
        ("MaximumTotalSize", c_ulong),
        ("RemoteAddress", c_ubyte * ETHER_ADDR_LENGTH),
        ("LocalAddress", c_ubyte * ETHER_ADDR_LENGTH),
        ("ProtocolBufferLength", c_ulong),
        ("ProtocolBuffer", c_ubyte * RAS_LINK_BUFFER_LENGTH)
    ]

class RAS_LINKS(Structure):
    _fields_ = [
        ("nNumberOfLinks", c_ulong),
        ("RasLinks", RAS_LINK_INFO * RAS_LINKS_MAX)
    ]

class TCPUDP_FILTER(Structure):
    _fields_ = [
        ("m_ValidFields", c_ulong),
        ("m_SourcePort", PORT_RANGE),
        ("m_DestPort", PORT_RANGE)
    ]

class TRANSPORT_LAYER(Union):
    _fields_ = [
        ("m_TcpUdp", TCPUDP_FILTER)
    ]

class TRANSPORT_LAYER_FILTER(Structure):
    _fields_ = [
        ("m_dwUnionSelector", c_ulong),
        ("u", TRANSPORT_LAYER)
    ]

class STATIC_FILTER(Structure):
    _fields_ = [
        ("m_Adapter", c_ulonglong),
        ("m_dwDirectionFlags", c_ulong),
        ("m_FilterAction", c_ulong),
        ("m_ValidFields", c_ulong),
        ("m_LastReset", c_ulong),
        ("m_Packets", c_ulonglong),
        ("m_Bytes", c_ulonglong),
        ("m_DataLinkFilter", DATA_LINK_LAYER_FILTER),
        ("m_NetworkFilter", NETWORK_LAYER_FILTER),
        ("m_TransportFilter", TRANSPORT_LAYER_FILTER)
    ]

class STATIC_FILTER_TABLE(Structure):
    _fields_ = [
        ("m_TableSize", c_ulong),
        ("m_StaticFilters", STATIC_FILTER * ANY_SIZE)
    ]

class TCP_AdapterList(Structure):
    _fields_ = [
        ("m_nAdapterCount", c_ulong),
        ("m_szAdapterNameList", (c_ubyte * ADAPTER_NAME_SIZE) * ADAPTER_LIST_SIZE),
        ("m_nAdapterHandle", c_void_p * ADAPTER_LIST_SIZE),
        ("m_nAdapterMediumList", c_uint * ADAPTER_LIST_SIZE),
        ("m_czCurrentAddress", (c_ubyte * ETHER_ADDR_LENGTH) * ADAPTER_LIST_SIZE),
        ("m_usMTU", c_ushort * ADAPTER_LIST_SIZE)
    ]
