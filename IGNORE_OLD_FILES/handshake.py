from bleak import BleakScanner
import asyncio

async def scan():
	devices = await BleakScanner.discover()
	for d in devices:
		print(f"Name: {d.name}, Address: {d.address}")
		
asyncio.run(scan())

#TARGET_MAC

FILE = "./home/jack/Desktop/project/test1.png"

def send_file():
	try:
		subprocess.run([
			"obexftp",
			"--bluetooth", TARGET_MAC,
			"--put", FILE
		], check=True)
		print("Successful File Transfer")
	except subprocess.CalledProcessError:
		print("Failed to complete File Transfer")


