import socket
import time
import threading
import curses
from logger import log_open_port
from recommendations import get_recommendations
from port_interaction import interact_with_port, send_payload

open_ports = []

def scan_port(target, port, stdscr):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    result = s.connect_ex((target, port))  # 0 means the port is open
    if result == 0:
        open_ports.append(port)
        log_open_port(port)
        interact_with_port(target, port)
        send_payload(target, port)  # Send payload to the open port
        stdscr.addstr(f"\rPort {port} is OPEN\n")
        stdscr.refresh()
    s.close()

def scan_ports(target, start_port, end_port, stdscr):
    threads = []
    for port in range(start_port, end_port + 1):
        thread = threading.Thread(target=scan_port, args=(target, port, stdscr))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

def display_results(target):
    if open_ports:
        print(f"\nThe following ports are open on {target}:")
        for port in open_ports:
            print(f"Port {port}")
            get_recommendations(port)  # Get recommendations based on open ports
    else:
        print(f"\nNo open ports found on {target}.")

def user_input():
    target = input("Enter the target IP or hostname to scan: ")
    start_port = int(input("Enter the starting port to scan: "))
    end_port = int(input("Enter the ending port to scan: "))
    return target, start_port, end_port

if __name__ == "__main__":
    # Initialize the curses window
    stdscr = curses.initscr()
    curses.cbreak()
    stdscr.clear()

    target, start_port, end_port = user_input()
    print(f"Starting scan on {target} from port {start_port} to {end_port}")
    start_time = time.time()
    scan_ports(target, start_port, end_port, stdscr)
    end_time = time.time()
    print(f"Scan completed in {end_time - start_time:.2f} seconds.")
    display_results(target)

    # Clean up curses settings
    curses.endwin()
