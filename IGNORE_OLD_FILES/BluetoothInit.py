import subprocess
import time
import re
import os

SEND_DIR = '/home/jack/Desktop/project/files'
TARGET_NAME = 'Jacks S25 Ultra'

def run_cmd(cmd):
	result = subprocess.run(cmd, capture_output=True, text=True)
	return result.stdout
	
def find_phone_mac():
	print("Scanning for Devices")
	
	scan = subprocess.Popen(["bluetoothctl", "scan", "on"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
	
	start = time.time()
	mac=None
	
	while time.time() - start < 15:
		line = scan.stdout.readline()
		if not line:
			continue
		
		print(line.strip())
		
		if TARGET_NAME in line:
			match = re.search(r"([0-9A-F:]{17})", line)
			if match:
				mac = match.group(1)
				print(f"Found Phone: {mac}")
				break
	
	scan.terminate()
	return mac
	
	#scan.stdin.write("scan on\n")
	#scan.stdin.flush()
	
	time.sleep(10)
	
	scan.stdin.write("scan off\n")
	scan.stdin.flush()
	
	output = scan.communicate()[0]
	
	for line in output.split("\n"):
		if TARGET_NAME in line:
			match = re.search(r"([0-9A-F:]{17})", line)
			if match:
				mac = match.group(1)
				print(f"Found phone: {mac}")
				return mac
				
	print("Phone not found...")
	return None
	
def pair_and_trust(mac):
	print("Pairing and Trusting phone...")
	
	commands = f"""
	pair {mac}
	trust {mac}
	connect {mac}
	quit
	"""
	
	subprocess.run(["bluetoothctl"], input=commands, text=True)
	
def find_OBEX_channel(mac):
	print("Finding OBEX channel for file transfer")
	
	output = run_cmd(["sdptool", "browse", mac])
	
	lines = output.split("\n")
	for i, line in enumerate(lines):
		if "OBEX Object Push" in line:
			for j in range(i, i+10):
				if "Channel:" in lines[j]:
					channel = re.search(r"\d+", lines[j]).group()
					print(f"Found OBEX channel: {channel}")
					return channel
					
	print("Defaulting to channel 9")
	return "9"
	
def bluetooth_connect(mac):
	subprocess.run(["rfkill", "block", "bluetooth"])
	time.sleep(1)
	
	subprocess.run(["rfkill", "unblock", "bluetooth"])
	time.sleep(2)
	
	commands = f"""
	power on
	connect {mac}
	"""
	
	subprocess.run(["bluetoothctl"], input=commands, text=True)
	
	time.sleep(5)
	
	subprocess.run(["quit"])
		
def send_file(mac, channel, filepath):
	print(f"Sending {filepath} via channel {channel}")
	
	result = subprocess.run([
		"obexftp",
		"--bluetooth", mac,
		"--channel", channel,
		"-p", filepath
	])
	
	print(result.stdout)
	print(result.stderr)
	
	return result.returncode == 0
	
def main():
	mac = None
	channel = None
	sent_files = set()
	attempt = 0
	for attempts in range(50):
		if not mac:
			mac = find_phone_mac()
		if not mac:
			time.sleep(2)
		if mac:
			break
			
	pair_and_trust(mac)
	channel = find_OBEX_channel(mac)
		
	bluetooth_connect(mac)
	
	for filename in os.listdir(SEND_DIR):
		filepath = os.path.join(SEND_DIR, filename)
		
		if filepath not in sent_files:
			success = send_file(mac, channel, filepath)
				
			if success:
				sent_files.add(filepath)
			else:
				print("Retry later!")
			
	time.sleep(5)
	
if __name__ == "__main__":
	main()
