# logger.py
import datetime

def log_open_port(port, service):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] Open Port Found: {port} - {service}\n"
    
    with open("scan_results.log", "a") as log_file:
        log_file.write(log_entry)
    
    print(log_entry)
