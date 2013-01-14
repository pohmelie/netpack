from .py3compat import int2byte


def int_to_bin(number, width=32, **kw):
    r"""
    Convert an integer into its binary representation in a bytes object.
    Width is the amount of bits to generate. If width is larger than the actual
    amount of bits required to represent number in binary, sign-extension is
    used. If it's smaller, the representation is trimmed to width bits.
    Each "bit" is either '\x00' or '\x01'. The MSBit is first.

    Examples:

        >>> int_to_bin(19, 5)
        b'\x01\x00\x00\x01\x01'
        >>> int_to_bin(19, 8)
        b'\x00\x00\x00\x01\x00\x00\x01\x01'
    """
    endian = kw.get("endian", "big")
    if number < 0:
        number += 1 << width
    if endian == "big":
        i, adder = width - 1, -1
    else:
        i, adder = 0, 1
    bits = bytearray(width)
    while number and i >= 0 and i < width:
        bits[i] = number & 1
        number >>= 1
        i = i + adder
    return bytes(bits)


_bit_values = {
    0: 0,
    1: 1,
    48: 0, # '0'
    49: 1, # '1'

    # The following are for Python 2, in which iteration over a bytes object
    # yields single-character bytes and not integers.
    '\x00': 0,
    '\x01': 1,
    '0': 0,
    '1': 1,
    }

def bin_to_int(bits, signed=False, **kw):
    r"""
    Logical opposite of int_to_bin. Both '0' and '\x00' are considered zero,
    and both '1' and '\x01' are considered one. Set sign to True to interpret
    the number as a 2-s complement signed integer.
    """
    if kw.get("endian", "big") == "little":
        bits = bits[::-1]
    number = 0
    bias = 0
    ptr = 0
    if signed and _bit_values[bits[0]] == 1:
        bits = bits[1:]
        bias = 1 << len(bits)
    for b in bits:
        number <<= 1
        number |= _bit_values[b]
    return number - bias


def swap_bytes(bits, bytesize=8):
    r"""
    Bits is a b'' object containing a binary representation. Assuming each
    bytesize bits constitute a bytes, perform a endianness byte swap. Example:

        >>> swap_bytes(b'00011011', 2)
        b'11100100'
    """
    i = 0
    l = len(bits)
    output = [b""] * ((l // bytesize) + 1)
    j = len(output) - 1
    while i < l:
        output[j] = bits[i : i + bytesize]
        i += bytesize
        j -= 1
    return b"".join(output)


_char_to_bin = {"big":{}, "little":{}}
_bin_to_char = {"big":{}, "little":{}}
_reverse = lambda x: (x * 0x0202020202 & 0x010884422010) % 1023
for i in range(256):
    ch = int2byte(i)
    bin = int_to_bin(i, 8)
    # Populate with for both keys i and ch, to support Python 2 & 3
    _char_to_bin["big"][ch] = bin
    _char_to_bin["big"][i] = bin
    _bin_to_char["big"][bin] = ch

    ch = int2byte(_reverse(i))
    bin = int_to_bin(_reverse(i), 8)
    _char_to_bin["little"][ch] = bin
    _char_to_bin["little"][i] = bin
    _bin_to_char["little"][bin] = ch

print(_char_to_bin["big"][1], _char_to_bin["little"][1])

def encode_bin(data, **kw):
    """
    Create a binary representation of the given b'' object. Assume 8-bit
    ASCII. Example:

        >>> encode_bin('ab')
        b"\x00\x01\x01\x00\x00\x00\x00\x01\x00\x01\x01\x00\x00\x00\x01\x00"
    """
    print(data, kw)
    endian = kw.get("endian", "big")
    return b"".join(_char_to_bin[endian][ch] for ch in data)

def decode_bin(data, **kw):
    """
    Locical opposite of decode_bin.
    """
    endian = kw.get("endian", "big")
    if len(data) & 7:
        raise ValueError("Data length must be a multiple of 8")
    i = 0
    j = 0
    l = len(data) // 8
    chars = [b""] * l
    while j < l:
        chars[j] = _bin_to_char[endian][data[i:i+8]]
        i += 8
        j += 1
    return b"".join(chars)
