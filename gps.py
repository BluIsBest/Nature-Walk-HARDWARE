import gpsd
import time

def connect_gps():
    gpsd.connect()

def get_gps(timeout=5):
    """
    Returns (lat, lon, timestamp)
    Waits up to `timeout` seconds for a valid fix.
    """
    start_time = time.time()

    while time.time() - start_time < timeout:
        try:
            packet = gpsd.get_current()

            if packet.mode >= 2:  # 2D fix or better
                return {
                    "latitude": packet.lat,
                    "longitude": packet.lon,
                    "timestamp": packet.time  # ISO timestamp from GPS
                }

        except Exception:
            pass

        time.sleep(0.2)

    return None
