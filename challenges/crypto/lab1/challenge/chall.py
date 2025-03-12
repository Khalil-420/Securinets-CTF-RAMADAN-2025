from secrets import a, b, flag
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

p = 147436102331921462525077505327436322903434762181746387293671718134777175598604600519552562108940384682379605681740774640829435258833160269822836052749565320913642712865010418762455653119035743120517740824800409493174162289163676564818453559854669574054222001780349765481237757389048809178551796365923020013193
g = 5



A = pow(g, a, p)
B = pow(g, b, p)

S = pow(A, b, p)


key = hashlib.sha256(str(S).encode()).digest() 
cipher = AES.new(key, AES.MODE_ECB) 
encrypted_data = cipher.encrypt(pad(flag.encode(), AES.block_size)) 

out = "A = {0} \nB = {1} \nP = {2} \nCipherText = {3} \n".format(A,B,p,encrypted_data.hex())
open('output.txt','w').write(out)