from construct.protocols.layer4.tcp import tcp_header
from construct.protocols.layer3.ipv4 import IpAddress, ProtocolEnum, ipv4_header
from construct import *


def checksum(m):
    m = m + bytes((0,))
    cs = sum(map(lambda i: (m[i] << 8) + m[i + 1], range(0, len(m) - 1, 2)))
    return ((cs >> 16) + (cs & 0xffff)) ^ 0xffff

def IPchecksum(ip):
    ip.header.checksum = 0
    ip.header.checksum = checksum(ipv4_header.build(ip.header))

psh = Struct(None,
        IpAddress("src"),
        IpAddress("dst"),
        ProtocolEnum(UBInt16("protocol")),
        UBInt16("tcplen")
    )
def TCPchecksum(ip):
    tcp = ip.next
    tcp.header.checksum = 0
    pshbin = psh.build(Container(
        src = ip.header.source,
        dst = ip.header.destination,
        protocol = ip.header.protocol,
        tcplen = ip.header.total_length - ip.header.header_length)
    )
    tcp.header.checksum = checksum(pshbin + tcp_header.build(tcp.header) + tcp.next)

def recalculatechecksums(ip):
    IPchecksum(ip)
    TCPchecksum(ip)

if __name__ == "__main__":
    from ipstack import ip_stack
    b = bytes.fromhex("00093bf01a40000a3bf016700800450002402e04000073061da86da7825b0a00000a172b0a76a8977e87d64c993e5010010050c500001732f7468a6ae4c9b605ec06886de7f3b7d734871748b54ec89b4f4cde5f307e2a75a687c42aa7eb61bd8ea953bb5c9311cedcf453323d3176f02d650d0c9db0291cadcf8fa6b623eee2bd64ea6c43aa24c00c6c0d5d7bbaeb8a195aca5c0cfb915897f1a57c8cabfb345ad0fbbd67a26252475982437b6e19221f09a763c3a29eabc2c892036be579db677dd0409e6b207e39cd26c2757b2295946dae0e6f4c7f7cca729e44eddd46b4d3494db325f1ca4c2aa88cc437e8d1007a0c9386738684fba5a0416611a17c81e23d8e6ebfceececf1d4b4be12e17802b4813335c27ad5f0ec5051320032c95a516f2ecef6abdab09f68d586ebb8b2a6d009bdc589b84d6e43c79fb263bf4860e1b2af27c47e51fd3abc2d851417bcccf39d844087b257fed67c211013da14398528bfce29f72a485d7409742a0c822a85f952e25e1e290fa80d53cba749b94f7a8e46ea8a71e3c727bfef0f2be2ec13abe265eb47af3514d54e5da1dfb5bc6a8252bbf4620b8febad6b57332e5fbbbe406d3b4ebedd5b92ef8aaff80f55f98832a0dc207b7993fe9c550440ccfc4fa78aff575e63a6861dd99e9f603c7a37fe82cfa35b8adae194bffa42f3e63d890fc3099df1adf620d3ff869ce4a99caa54e27c54aa26ec5b537f5b00478363535e18d95f40439a24e164548305fe244cca6b24f53a189743a62fec07ba10ed4986fd20f8a6920218f1667523c4f509b78859fa350b83a684db8e596e0b1c68")
    eth = ip_stack.parse(b)
    ip = eth.next
    print("default checksums: ip = {:x}, tcp = {:x}".format(ip.header.checksum, ip.next.header.checksum))
    recalculatechecksums(ip)
    print("recalculated checksums: ip = {:x}, tcp = {:x}".format(ip.header.checksum, ip.next.header.checksum))
