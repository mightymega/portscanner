# port_interaction.py

import socket

def interact_with_port(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(2)
            s.connect((ip, port))
            s.sendall(b"Hello, are you open?\n")
            response = s.recv(1024)
            return response.decode("utf-8") if response else "No response"
    except Exception as e:
        return f"Could not interact with port {port}: {str(e)}"


def send_payload(ip, port, payload):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(2)
            s.connect((ip, port))
            s.sendall(payload.encode())
            response = s.recv(1024)
            return response.decode("utf-8") if response else "No response"
    except Exception as e:
        return f"Failed to send payload to port {port}: {str(e)}"
