import requests
import os

GPX_SWITH_FILE = 'switch.gpx'
ACCESS_POINT = 'http://192.168.0.128/gpx'


def buildSinglePointGpx(lat, lng):
	gpx = """<?xml version="1.0" encoding="UTF-8" ?>
<gpx version="1.1">
	<wpt lat="{lat}" lon="{lng}"></wpt>
</gpx>
"""
	return gpx.format(lat=lat, lng=lng)

def updatePoint(lat, lng):
	with open(GPX_SWITH_FILE, 'w') as writer:
		writer.write(buildSinglePointGpx(lat, lng))

def getPosition():
	r = requests.get(ACCESS_POINT)# 'a,b'
	pointsStr = r.text
	points = pointsStr.split(',')
	return (float(points[0]), float(points[1]))
	

def main():
	while True:
		points = getPosition()
		updatePoint(points[0], points[1])
		#os.system('osascript autoClick.scpt')


if __name__ == '__main__':
	main()