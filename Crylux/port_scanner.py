import socket
import threading
import time
from queue import Queue
from pystyle import Colorate, Colors, Center

# Stylized banner
banner = r"""
██████╗  ██████╗ ██████╗ ████████╗    ███████╗ ██████╗ █████╗ ███╗   ██╗███╗   ██╗███████╗██████╗ 
██╔══██╗██╔═══██╗██╔══██╗╚══██╔══╝    ██╔════╝██╔════╝██╔══██╗████╗  ██║████╗  ██║██╔════╝██╔══██╗
██████╔╝██║   ██║██████╔╝   ██║       ███████╗██║     ███████║██╔██╗ ██║██╔██╗ ██║█████╗  ██████╔╝
██╔═══╝ ██║   ██║██╔══██╗   ██║       ╚════██║██║     ██╔══██║██║╚██╗██║██║╚██╗██║██╔══╝  ██╔══██╗
██║     ╚██████╔╝██║  ██║   ██║       ███████║╚██████╗██║  ██║██║ ╚████║██║ ╚████║███████╗██║  ██║
╚═╝      ╚═════╝ ╚═╝  ╚═╝   ╚═╝       ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝
"""
subtitle = "baka port scanner by vantixt"

print(Colorate.Horizontal(Colors.purple_to_blue, Center.XCenter(banner)))
print(Colorate.Horizontal(Colors.purple_to_blue, Center.XCenter(subtitle)))

# Input
target = input(Colorate.Horizontal(Colors.purple_to_blue, "[?] Enter Target IP or Hostname: "))
start_port = int(input(Colorate.Horizontal(Colors.purple_to_blue, "[?] Start Port (1-65535): ")))
end_port = int(input(Colorate.Horizontal(Colors.purple_to_blue, "[?] End Port (1-65535): ")))
thread_count = int(input(Colorate.Horizontal(Colors.purple_to_blue, "[?] Threads (Recommended: 100): ")))
timeout = float(input(Colorate.Horizontal(Colors.purple_to_blue, "[?] Timeout (Seconds, e.g., 0.5): ")))

# Host resolution
try:
    target_ip = socket.gethostbyname(target)
    print(Colorate.Horizontal(Colors.purple_to_blue, f"\n[+] Resolved {target} to {target_ip}"))
except socket.gaierror:
    print(Colorate.Horizontal(Colors.purple_to_blue, f"\n[!] Error: Could not resolve {target}"))
    exit()

# Queue and status
queue = Queue()
open_ports = []
scanned_ports = 0
print_lock = threading.Lock()

# Port scan logic
def scan_port(port):
    global scanned_ports
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((target_ip, port))
        if result == 0:
            with print_lock:
                print(Colorate.Horizontal(Colors.purple_to_blue, f"[+] Port {port} is OPEN"))
                open_ports.append(port)
        sock.close()
    except Exception as e:
        with print_lock:
            print(Colorate.Horizontal(Colors.purple_to_blue, f"[-] Error scanning port {port}: {str(e)}"))
    finally:
        with print_lock:
            scanned_ports += 1
            if scanned_ports % 100 == 0:
                print(Colorate.Horizontal(Colors.purple_to_blue, f"[*] Scanned {scanned_ports} ports..."))

# Thread worker
def worker():
    while not queue.empty():
        port = queue.get()
        scan_port(port)
        queue.task_done()

# Queue ports
for port in range(start_port, end_port + 1):
    queue.put(port)

# Start scan
print(Colorate.Horizontal(Colors.purple_to_blue,
      f"\n[+] Starting scan on {target_ip} (ports {start_port}-{end_port})"))
start_time = time.time()

threads = []
for _ in range(thread_count):
    t = threading.Thread(target=worker, daemon=True)
    threads.append(t)
    t.start()

# Wait or interrupt
try:
    while any(t.is_alive() for t in threads):
        time.sleep(0.1)
except KeyboardInterrupt:
    print(Colorate.Horizontal(Colors.purple_to_blue, "\n[!] Scan interrupted by user!"))
    exit()

# Completion
queue.join()
for t in threads:
    t.join()

# Results
print(Colorate.Horizontal(Colors.purple_to_blue, "\n[!] SCAN COMPLETE!"))
print(Colorate.Horizontal(Colors.purple_to_blue, f"[!] Time taken: {time.time() - start_time:.2f} seconds"))
print(Colorate.Horizontal(Colors.purple_to_blue, f"[!] Scanned ports: {scanned_ports}"))
if open_ports:
    print(Colorate.Horizontal(Colors.purple_to_blue, f"[!] Open ports found: {sorted(open_ports)}"))
else:
    print(Colorate.Horizontal(Colors.purple_to_blue, "[!] No open ports found."))
