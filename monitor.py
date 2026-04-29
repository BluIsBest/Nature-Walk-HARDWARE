import subprocess
import threading

def monitor_utilization(log_list):
    proc = subprocess.Popen(["tegrastats"], stdout=subprocess.PIPE, text=True)

    for line in proc.stdout:
        log_list.append((time.time(), line))
