import threading
import time

from camera import capture_burst, variance_of_laplacian, select_sharpest
# from predictImage import 
from exporter import append_to_json
from gps import get_gps
from monitor import monitor_utilization

def main():
    util_log = []

    monitor_thread = threading.Thread(
        target=monitor_utilization,
        args=(util_log,),
        daemon=True
    )
    monitor_thread.start()

    lat, lon = get_gps()

    images, timestamps = capture_burst(5)

    best_img, idx, scores = select_sharpest(images)
    best_timestamp = timestamps[idx]

    result = classify(best_img)

    entry = {
        "latitude": lat,
        "longitude": lon,
        "timestamp": best_timestamp,
        "species_id": result["species_id"],
        "species_name": result["species_name"]
    }

    append_to_json("observations.json", entry)

    # optionally save utilization log
    append_to_json("utilization.json", util_log)

if __name__ == "__main__":
    main()
