import socket
import threading
import time
import sys
from recommendations import get_recommendations
from port_interaction import interact_with_port

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
    
# Function to scan an individual port
def scan_port(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            result = s.connect_ex((ip, port))
            
            if result == 0:
                print(f"\n[+] Port {port} is OPEN")
                recommendation = get_recommendations(port)
                print(f"[*] Recommendation: {recommendation}")

                response = interact_with_port(ip, port)
                print(f"[*] Response from port {port}: {response}")

    except Exception as e:
        print(f"\n[-] Error scanning port {port}: {str(e)}")

# Function to scan a range of ports with a progress animation
def scan_ports(ip, start_port, end_port):
    print(f"\n[*] Scanning {ip} from port {start_port} to {end_port}...\n")
    threads = []

    for port in range(start_port, end_port + 1):
        for progress in range(0, 101, 10):  # Increment progress in steps of 10%
            print_progress_bar(port, progress)
            time.sleep(0.05)  # Simulated delay for animation effect
        
        sys.stdout.write("\n")  # Move to a new line after progress bar completion

        thread = threading.Thread(target=scan_port, args=(ip, port))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

# Main function
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

        start_port = int(input("Enter the start port (default: 1): ") or 1)
        end_port = int(input("Enter the end port (default: 65535): ") or 65535)

        scan_ports(ip, start_port, end_port)

    except KeyboardInterrupt:
        print("\n[-] Scan interrupted by user. Exiting.")

if __name__ == "__main__":
    main()
