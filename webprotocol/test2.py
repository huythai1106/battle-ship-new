import socket

bytedata = b"abcd"
x = int.from_bytes(bytedata, 'little')
print(x+2)