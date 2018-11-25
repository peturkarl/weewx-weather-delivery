import requests
import time
import json
import math
import moment
import cv2
from picamera import PiCamera
from datetime import datetime
from config import *

# Set font properties
font = cv2.FONT_HERSHEY_DUPLEX
font_color = (255,255,255)
font_size_on_image = 1.0

# Functions
def directionMap(windDirection):
	mapper = {
		"N" : "N",
		"NNE" : "NNA",
		"NE" : "NA",
		"ENE" : "ANA",
		"E" : "A",
		"ESE" : "ASA",
		"SE" : "SA",
		"SSE" : "SSA",
		"S" : "S",
		"SSW" : "SSV",
		"SW" : "SV",
		"WSW" : "VSV",
		"W" : "V",
		"WNW" : "VNV",
		"NW" : "NV",
		"NNW" : "NNV",
		"N/A": "NOT AVAIL"
	}
	try: 
		wind_direction = mapper[windDirection]
		return wind_direction
	except:
		print("Malformed wind_direction value from weewx controller, returning ERR")
		return "ERR"


###############################################
###         START OF APP LOGIC          #######
###############################################

# Fetch Weather data
try:
	with open(WEATHER_FILE) as f:
		weather_data = json.load(f)
except:
	print("Could not open weather_data file, make sure it has been setup. Quitting..")
	sys.exit()

# Initalize Camera
try:
	camera = PiCamera()
	camera.resolution = (IMAGE_WIDTH, IMAGE_HIGHT)
	camera.annotate_text_size = TEXT_SIZE
except:
	print("Could not open camera feed, make sure it has been connected and setup correctly. Quitting..")
	sys.exit()

try: 
	# Get temp value from file
	temperature_value = weather_data['outTemp']

	# Get date of weather data
	date_header = weather_data['datetime']

	# Get wind in ms and direction from helper function
	wind_value = weather_data['windSpeed']
	wind_direction = directionMap(weather_data['ordinal_compass'])
	
except: 
	print("Could not get weather data from file, has it been setup correctly?")

try:
	# initalize first picture so the camera can set the brightnes
	camera.capture('latest_image_from_camera.jpg', quality=IMAGE_QUALITY)
	time.sleep(1)
	camera.capture('latest_image_from_camera.jpg', quality=IMAGE_QUALITY)
	img = cv2.imread('latest_image_from_camera.jpg')
except: 
	print("Could not snap image from camera feed, make sure it has been connected and setup correctly. Quitting..")
	
# get image width height
ht, wd, channels = img.shape

# draw thick black line at top and bottom
# Python: cv2.line(img, pt1, pt2, color[, thickness[, lineType[, shift]]]
cv2.line(img,(0,0),(wd,0),(0,0,0), 75)
cv2.line(img,(0,ht),(wd,ht),(0,0,0), 75)

# add text at top and bottom of image
# Python: cv2.putText(img, text, org, fontFace, fontScale, color[, thickness[, lineType[, bottomLeftOrigin]]]) None
cv2.putText(img, HEADER_TEXT+' - '+ date_header, (10,30), font, font_size_on_image,font_color,1)
cv2.putText(img, wind_direction + ' ' + wind_value + ' ' + temperature_value,(10,ht-10), font, font_size_on_image,font_color,1)

try:
	cv2.imwrite('latest_image_from_camera.jpg', img) # Save image
except: 
	print("Could not write camera image to file system, disk corrupted or full?. Quitting...")
	sys.exit()

# Upload procedure
try:
	files = {'userfile': open('latest_image_from_camera.jpg', 'rb')}
	requests.post(SERVER, files=files, auth=(USER, PASS))
except: 
	print("Could not POST image to server, is internet access available or page is down?")

# Close procedure
camera.close()
time.sleep(5)

# End logic
print(time.strftime("%a %d %B %Y %H:%M:%S", time.gmtime()) + " - Successfully uploaded image to smartcam with weather data")
