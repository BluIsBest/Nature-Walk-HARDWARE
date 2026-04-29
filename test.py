# import gps
from camera import capture_burst, variance_of_laplacian, select_sharpest

capture_burst()

# session = gps.gps(mode=gps.WATCH_ENABLE)

"""
try:
	while 0 == session.read():
		if not (gps.MODE_SET & session.valid):
			continue
		
		print('Mode: %s(%d) Time: ' %
			(("Invalid", "NO_FIX", "2D", "3D")[session.fix.mode],
			session.fix.mode),end="")
		if gps.TIME_SET & session.valid:
			print(session.fix.time, end="")
		else:
			print('n/a',end="")
		
		if ((gps.isfinite(session.fix.latitude) and gps.isfinite(session.fix.longitude))):
			print(" Lat %.6f Lon %.6f" % 
				(session.fix.latitude, session.fix.longitude))
		else:
			print(" Lat n/a Lon n/a")
			
except KeyboardInterrupt:
	print('')
	
session.close()
exit(0)
"""

