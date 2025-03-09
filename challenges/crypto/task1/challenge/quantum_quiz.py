#!/usr/bin/env python3
import sys
import socket

# Fancy ASCII art banner
BANNER = """
  █████   █    ██  ▄▄▄       ███▄    █ ▄▄▄█████▓ █    ██  ███▄ ▄███▓
▒██▓  ██▒ ██  ▓██▒▒████▄     ██ ▀█   █ ▓  ██▒ ▓▒ ██  ▓██▒▓██▒▀█▀ ██▒
▒██▒  ██░▓██  ▒██░▒██  ▀█▄  ▓██  ▀█ ██▒▒ ▓██░ ▒░▓██  ▒██░▓██    ▓██░
░██  █▀ ░▓▓█  ░██░░██▄▄▄▄██ ▓██▒  ▐▌██▒░ ▓██▓ ░ ▓▓█  ░██░▒██    ▒██ 
░▒███▒█▄ ▒▒█████▓  ▓█   ▓██▒▒██░   ▓██░  ▒██▒ ░ ▒▒█████▓ ▒██▒   ░██▒
░░ ▒▒░ ▒ ░▒▓▒ ▒ ▒  ▒▒   ▓▒█░░ ▒░   ▒ ▒   ▒ ░░   ░▒▓▒ ▒ ▒ ░ ▒░   ░  ░
 ░ ▒░  ░ ░░▒░ ░ ░   ▒   ▒▒ ░░ ░░   ░ ▒░    ░    ░░▒░ ░ ░ ░  ░      ░
   ░   ░  ░░░ ░ ░   ░   ▒      ░   ░ ░   ░       ░░░ ░ ░ ░      ░   
    ░       ░           ░  ░         ░             ░            ░    
                        
				 			by Mrx0rd
"""

# List of quantum-themed questions and answers
QUIZ = [
    ("How are the special bits called in quantum computing? ", "qubit"),
    ("What is the name of the graphical representation of the qubit? ", "bloch sphere"),
    ("In what state is a qubit which is neither 1 nor 0? ", "superposition"),
    ("What do you call 2 qubits which have interacted and are now in a weird state in which they are correlated? ", "entangled"),
    ("What do you call the notation used in Quantum Computing where qubits are represented like this: |0> or |1>? ", "dirac"),
    ("What gate would you use to put a qubit in a superposition? ", "hadamard"),
    ("What gate would you use to entangle 2 qubits? ", "controlled not"),
    ("What gate would you use to 'flip' a qubit's phase in a superposition? ", "pauli-z"),
    ("What's the full name of the physicist who invented the X, Y and Z gates? ", "wolfgang pauli"),
    ("What are quantum gates represented by (in dirac notation)? ", "unitary matrix"),
    ("How do you represent a qubit |1> put in a superposition (in dirac)? ", "|->"),
    ("Will a superposition break if measured? ", "yes"),
    ("Can you take a qubit out of a superposition with a Hadamard gate? ", "yes"),
    ("If you measure a qubit in a superposition, what's the average chance of measuring |0>? ", "0.5"),
    ("What's the name of the famous paradox which demonstrates the problem of decoherence? ", "schrodinger's cat"),
    ("Will particles always measure the same when entangled? ", "no"),
    ("Will entangled qubits violate Bell's Inequality? ", "yes"),
    ("Does the following state present 2 entangled qubits? 1/sqrt(2)(|10> + |11>)? ", "no"),
    ("Does the following state present 2 entangled qubits? 1/sqrt(2)(|10> + |01>)? ", "yes"),
    ("Can 2 entangled qubits ever get untangled? ", "yes")
]

# The flag to be revealed upon completion
FLAG = "Securinets{Qu4ntwm_Tantrum_M1llionar3}"

def handle_client(client_socket):
    """Handle client connection and quiz logic."""
    try:
        # Send the welcome banner
        client_socket.send(f"{BANNER}\nWelcome to the Quantum CTF Challenge!\n\n".encode())

        # Iterate through each question
        for i, (question, correct_answer) in enumerate(QUIZ, 1):
            # Send question with a newline for answer prompt
            client_socket.send(f"Question {i}/{len(QUIZ)}: {question}\nYour answer: ".encode())
            
            # Receive the client's answer
            user_answer = client_socket.recv(1024).decode().strip().lower()

            # Check if the answer matches
            if user_answer != correct_answer:
                client_socket.send("❌ Wrong answer! Connection closed.\n".encode())
                client_socket.close()
                return

            # Send confirmation for correct answer
            client_socket.send("✅ Correct!\n\n".encode())

        # All answers correct, send the flag
        client_socket.send(f"🎉 Congratz! You made it! ;)\nHere's your flag: {FLAG}\n".encode())

    except Exception as e:
        client_socket.send(f"⚠️ Error: {str(e)}\n".encode())
    finally:
        client_socket.close()

def main():
    """Set up and run the server."""
    # Configure the server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 1337))  # Bind to all interfaces on port 12345
    server.listen(1)
    print(" Server listening on port 1337...")

    # Accept incoming connections
    while True:
        client_socket, addr = server.accept()
        print(f"Connection from {addr}")
        handle_client(client_socket)

if __name__ == "__main__":
    main()
