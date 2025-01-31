import socket
import threading
import time
import sys
from recommendations import get_recommendations
from port_interaction import interact_with_port

# High-risk ports commonly targeted by hackers on Android
HIGH_RISK_PORTS = [5555, 22, 80, 443, 23, 2323, 5900, 5353, 8080, 8443]

# ANSI color codes for green text
GREEN = "\033[92m"
RESET = "\033[0m"

def print_progress_bar(port, progress):
    """Displays a dynamic progress bar for port scanning."""
    bar_length = 10  # Number of '#' characters in the bar
    filled_length = int(bar_length * progress // 100)
    
    bar = f"{GREEN}{'#' * filled_length}{RESET}{'.' * (bar_length - filled_length)}"
    sys.stdout.write(f"\r[Scanning Port {port}] [{bar}] {progress}%")
    sys.stdout.flush()

def scan_port(ip, port):
    """Scans a single port and prints results after animation."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            result = s.connect_ex((ip, port))

            # Simulated progress bar (fills to 100%)
            for progress in range(0, 101, 10):
                print_progress_bar(port, progress)
                time.sleep(0.05)  # Simulated delay for effect
            
            sys.stdout.write("\n")  # Move to new line after progress bar

            if result == 0:
                print(f"[+] Port {port} is OPEN")
                recommendation = get_recommendations(port)
                print(f"[*] Recommendation: {recommendation}")

                response = interact_with_port(ip, port)
                print(f"[*] Response from port {port}: {response}")
            else:
                print(f"[-] Port {port} is CLOSED")

    except Exception as e:
        print(f"\n[-] Error scanning port {port}: {str(e)}")

def scan_high_risk_ports(ip):
    """Scans only high-risk Android ports."""
    print(f"\n[*] Scanning {ip} for high-risk ports: {HIGH_RISK_PORTS}\n")
    threads = []

    for port in HIGH_RISK_PORTS:
        thread = threading.Thread(target=scan_port, args=(ip, port))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

def main():
    try:
        ip = input("Enter the target IP or hostname to scan: ").strip()
        if not ip:
            print("[-] No IP provided. Exiting.")
            return

        try:
            ip = socket.gethostbyname(ip)
        except socket.gaierror:
            print("[-] Invalid IP or hostname.")
            return

        scan_high_risk_ports(ip)

    except KeyboardInterrupt:
        print("\n[-] Scan interrupted by user. Exiting.")

if __name__ == "__main__":
    main()
