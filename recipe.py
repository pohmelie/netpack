def apply(fun, *iterables):
    for args in zip(*iterables):
        fun(*args)

def rev(x):
    if type(x) == str:
        return bytes().fromhex(x.replace(" ", ""))
    else:
        return " ".join(map("{:0>2x}".format, x))

if __name__ == "__main__":
    print(rev(b'\xa1\xd9\x00(H@\xf0\xb0\x00(k\x06'))
    print(rev(b'\xa1\xe9\x00\x90\xe0\xc80\xb0\x00(\xdc\x02'))
    print(rev(b'\xa1\xd1\x0008\xc8\xe8\xb0\x00\x187\x05'))
    print()
    print(rev(b'!28\xc8\xe8\x00\x00\x00\x00'))
    print(rev(b'!*H@\x00\x00\x00\x00'))
