#!/usr/bin/env python3

import sys

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

def main():
    print("Welcome to BRIKA!")
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
