import os,glob

categories = ["web","crypto","forensics","misc","pwn","reverse","osint","hardware","workshop"]

for category in categories:
    if os.path.exists(f"./{category}"):
        challenges = glob.glob(f"{category}/*")
        for challenge in challenges:
                print(f"[+] Installing challenge: {challenge}")
                os.system(f"python3 -m ctfcli challenge sync \"{challenge}\" && python3 -m ctfcli challenge verify \"{challenge}\"")    
    else:
        print(f"[-] Cant find : {category}")
        exit(1)

exit(0)
