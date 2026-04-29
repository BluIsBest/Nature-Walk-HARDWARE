import gpsd
import time
import json
import os

LOG_FILE = "data_log.json"

gpsd.connect()

def get_gps():
	try:
		packet = gpsd.get_current()
		return {
			"lat": packet.lat,
			"lon": packet.lon,
			"alt": packet.alt,
			"mode": packet.mode
		}
	except:
		return {
			"lat": None,
			"lon": None,
			"alt": None,
			"mode": 0,
		}

def load_log():
	if not os.path.exists(LOG_FILE):
		return []
	with open(LOG_FILE, "r") as f:
		try:
			return json.load(f)
		except:
			return []
			
def save_log(data):
	with open(LOG_FILE, "w") as f:
		json.dump(data, f, indent=2)

def log_event():
	timestamp = int(time.time())
	gps_data = get_gps()
	
	record = {
		"timestamp": timestamp,
		"gps": gps_data,
		"plant": {
			"name": None,
			"id": None,
		}
	}
	
	log = load_log()
	log.append(record)
