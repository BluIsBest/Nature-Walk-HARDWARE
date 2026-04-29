import cv2
import time

def gstreamer_pipeline():
    return (
        "nvarguscamerasrc ! "
        "video/x-raw(memory:NVMM), width=1920, height=1080, framerate=30/1 ! "
        "nvvidconv ! video/x-raw, format=BGRx ! "
        "videoconvert ! video/x-raw, format=BGR ! appsink"
    )

def capture_burst(n=5):
	cap = cv2.VideoCapture(gstreamer_pipeline(), cv2.CAP_GSTREAMER)

	images = []
	timestamps = []

	if not cap.isOpened():
    		raise RuntimeError("Camera failed to open")

	for i in range(n):
		ret, frame = cap.read()
		print(f"Frame {i}: ret={ret}")

		if ret:
			images.append(frame)
			timestamps.append(time.time())
		else:
			print(f"Failed to capture frame {i}")
            
	time.sleep(0.05)

	cap.release()

	if len(images) == 0:
		raise RuntimeError("No images captured")
    
	if len(images) < n:
		print(f"Warning: Only captured {len(images)} out of {n} frames")
	
	for i, img in enumerate(images):
		cv2.imshow(f"Frame {i}", img)
		cv2.waitKey(500)
    
	cv2.destroyAllWindows()

	return images, timestamps
    
def variance_of_laplacian(image):
	cv2.Laplacian(image, cv2.CV_64F).var()

def select_sharpest(images):
    	scores = [variance_of_laplacian(img) for img in images]
    	best_index = scores.index(max(scores))
    	return images[best_index], best_index, scores
    
def test():
	print("Working")
	
# For testing if camera is brought up proper	
# nvgstcapture-1.0

"""
test 
dmesg | grep -i imx219
gst-launch-1.0 nvarguscamerasrc ! nvoverlaysink OR nvgstcapture-1.0

if these dont work attempt
FDTOVERLAYS /boot/tegra234-p3767-camera-p3768-imx219-C.dtbo


FOR DUAL CAMERA USE
...imx219-dual.dtbo

"""
