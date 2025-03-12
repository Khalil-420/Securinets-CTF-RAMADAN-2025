import socket

HOST = '0.0.0.0'  # Listen on all interfaces
PORT = 1337       # Port for the nc connection
FLAG = "Securinets{Y0u_D3serV3_4_Br1KA}"

questions = [
    {"question": "what's the compromised host IP@", "answer": "10.10.10.102"},
    {"question": "List the suspicious DNS (example: DNS1_DNS2_DNS3)", "answer": "www.dropox.com_ucdd5d6bc9869417d2bbd7f22955.dl.dropboxusercontent.com_teleportfilmona.online"},
    {"question": "which DNS has the most http traffic with the victim", "answer": "teleportfilmona.online"},
    {"question": "In what file format the data is being exfiltrated", "answer": "zip"},
    {"question": "what's the IP@ this data is being sent to", "answer": "104.21.11.40"},
    {"question": "what's the malware family name", "answer": "LummaC2"},
    {"question": "what's the malware build date (dd-mm-yyyy)", "answer": "09-10-2023"},
    {"question": "what's the LID(Lumma ID)", "answer": "Zbbaau--Лакосте"},
    {"question": "what's the OS type and version of the infected system", "answer": "Windows 10 (10.0.19045)"},
    {"question": "what's the icon visible on the screenshot took from the system", "answer": "Recycle Bin"},
    {"question": "what's the md5 hash value of the stealed cookies file", "answer": "b0c1133c8e8d4d7c359249d4e3208cb5"}
]

def handle_client(conn):
    conn.sendall(b"Welcome to the Ultimate Malware Investigation\n")
    conn.sendall(b"Answer all questions correctly to receive the flag.\n\n")
    
    for idx, q in enumerate(questions):
        conn.sendall(f"Question {idx + 1}: {q['question']}\n".encode())
        conn.sendall(b"Your answer: ")
        answer = conn.recv(1024).decode().strip()
        
        if answer.lower() != q["answer"].lower():
            conn.sendall(b"Wrong answer. Try again later!\n")
            conn.close()
            return
    
    conn.sendall(b"Congratulations! You answered all questions correctly.\n")
    conn.sendall(f"Here is your flag: {FLAG}\n".encode())
    conn.close()

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((HOST, PORT))
        server.listen(1)
        print(f"Quiz server running on {HOST}:{PORT}")
        
        while True:
            conn, addr = server.accept()
            print(f"Connection from {addr}")
            handle_client(conn)

if __name__ == "__main__":
    main()
