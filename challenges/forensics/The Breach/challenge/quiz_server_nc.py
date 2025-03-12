#!/usr/bin/env python3

import sys

FLAG = "Securinets{Th1s_1s_N3tw0rk_An4lys1s}"

questions = [
    {"question": "what is the date of the attack", "answer": "Wed, 05 Mar 2025"},
    {"question": "First Victim IP and Mac Address , Example : 127.0.0.1:ff:ff:ff:ff:ff:ff", "answer": "192.168.110.135_00:0c:29:a7:68:2e"},
    {"question": "First Victim Hostname", "answer": "WIN-PIF43K5LIED"},
    {"question": "ping duration", "answer": str(97.918068884 - 93.81658597)},
    {"question": "hacker IP address", "answer": "192.168.110.128"},
    {"question": "Hacker Machine hostname", "answer": "kali"},
    {"question": "the hackers internet certificate serialNumber", "answer": "03836f556311c3d89976bb342fa0dd3d262c"},
    {"question": "tool used in the scaning + Number of packet identifying it", "answer": "nmap_46897"},
    {"question": "vulnerable Web Server IP", "answer": "192.168.110.136"},
    {"question": "Vulnerable Web Server Hostname", "answer": "VICTIME"},
    {"question": "what is the web server version", "answer": "Apache/2.2.11"},
    {"question": "what is the vulnerable web application", "answer": "Moodle"},
    {"question": "what is the session token", "answer": "gq9e9ks4gd4tvfhg63keg78qj6"},
    {"question": "what is the admin password", "answer": "SeCrEt"},
    {"question": "what method did the hacker use", "answer": "Bruteforce"},
    {"question": "what tool did the hacker use", "answer": "burpsuite"},
    {"question": "victim email address", "answer": "jpyche@live.fr"}
]

def main():
    print("Answer all questions correctly to receive the flag.\n")

    for idx, q in enumerate(questions):
        print(f"Question {idx + 1}: {q['question']}")
        print("Your answer: ", end="")
        sys.stdout.flush()
        
        answer = sys.stdin.readline().strip()
        if answer.lower() != q["answer"].lower():
            print("Wrong answer. Try again later!")
            return

    print("Congratulations! You answered all questions correctly.")
    print(f"Here is your flag: {FLAG}")

if __name__ == "__main__":
    main()
