import socket
import threading
from recommendations import get_recommendations
from port_interaction import interact_with_port, send_payload

# Function to scan a specific port
def scan_port(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)  # 1 second timeout for each connection attempt
            result = s.connect_ex((ip, port))
            if result == 0:
                print(f"[+] Port {port} is OPEN")
                recommendation = get_recommendations(port)
                print(f"[*] Recommendation: {recommendation}")

                # Try interacting with the open port
                response = interact_with_port(ip, port)
                print(f"[*] Response from port {port}: {response}")

    except Exception as e:
        print(f"[-] Error scanning port {port}: {str(e)}")

# Function to scan a range of ports
def scan_ports(ip, start_port, end_port):
    print(f"[*] Scanning {ip} from port {start_port} to {end_port}...\n")
    threads = []
    
    for port in range(start_port, end_port + 1):
        thread = threading.Thread(target=scan_port, args=(ip, port))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

# Main function
def main():
    # Make sure input is accepted properly
    try:
        ip = input("Enter the target IP or hostname to scan: ").strip()
        if not ip:
            print("[-] No IP provided. Exiting.")
            return

        # Convert hostname to IP if needed
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
