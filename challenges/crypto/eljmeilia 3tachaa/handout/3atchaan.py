import random
import socket
import threading
from secret import p,q,x,h, flag

BANNER = """
 ██████╗ █████╗ ███╗   ███╗███████╗██╗     
██╔════╝██╔══██╗████╗ ████║██╔════╝██║     
██║     ███████║██╔████╔██║█████╗  ██║     
██║     ██╔══██║██║╚██╔╝██║██╔══╝  ██║     
╚██████╗██║  ██║██║ ╚═╝ ██║███████╗███████╗
 ╚═════╝╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝╚══════╝
"""

flag = "Securinets{fake_flag}"

def modinv(b, n):
    def xgcd(b, n):
        x0, x1, y0, y1 = 1, 0, 0, 1
        while n != 0:
            q, b, n = b // n, n, b % n
            x0, x1 = x1, x0 - q * x1
            y0, y1 = y1, y0 - q * y1
        return b, x0, y0
    g, x, _ = xgcd(b, n)
    if g == 1:
        return x % n

def enc(m):
    M = int.from_bytes(m, 'big')
    assert M < p, "Message too long"
    y = random.SystemRandom().randint(0, p-1)
    c1 = pow(g, y, p)
    c2 = (M * pow(h, y, p)) % p
    return c1, c2

def dec(c1, c2):
    s = pow(c1, x, p)
    M = (c2 * modinv(s, p)) % p
    byte_len = (M.bit_length() + 7) // 8
    return M.to_bytes(byte_len, 'big')

def handle_client(client_socket):
    try:
        client_socket.send(f"{BANNER}\nWhat do you want to do?\n[1] Login\n[2] Register\n> ".encode())
        choice = client_socket.recv(1024).decode().strip()
        
        if choice == "1":
            client_socket.send("Please input your access token: ".encode())
            token = client_socket.recv(1024).decode().strip()
            try:
                c1, c2 = map(lambda x: int(x, 16), token.split('_'))
                message = dec(c1, c2)
                user, role = message.split(b'#')
                user, role = user.decode(), role.decode()
                client_socket.send(f"Welcome {user}!\nYour role is '{role}'\n".encode())
                if role == "overlord":
                    client_socket.send(f"Here's your flag: {flag}\n".encode())
                client_socket.send("That's all, nothing else happening here.\n".encode())
            except ValueError:
                client_socket.send("Invalid token format. Use c1_c2 (hex values).\n".encode())
            except Exception as e:
                client_socket.send(f"Decryption failed: {str(e)}\n".encode())
        
        elif choice == "2":
            client_socket.send("Your username: ".encode())
            username = client_socket.recv(1024).decode().strip()
            client_socket.send("Your role: ".encode())
            role = client_socket.recv(1024).decode().strip()
            if role == "overlord":
                client_socket.send("Nope, you can't register as overlord!\n".encode())
            else:
                message = f"{username}#{role}".encode()
                c1, c2 = enc(message)
                client_socket.send(f"Here is your access token: \n".encode())
        
        else:
            client_socket.send("Invalid choice.\n".encode())
    
    except Exception as e:
        client_socket.send(f"Error: {str(e)}\n".encode())
    
    finally:
        client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("localhost", 1337))  
    server.listen(5)
    print("Server listening on localhost:1337...")
    while True:
        client_socket, _ = server.accept()
        threading.Thread(target=handle_client, args=(client_socket,)).start()

if __name__ == "__main__":
    start_server()
