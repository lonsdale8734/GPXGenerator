import requests
import os, sys

GPX_SWITH_FILE = 'switch.gpx'
ACCESS_POINT = 'http://192.168.0.128:9999/next'


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
	return r.json()


def main(toClick=False):
	lastPoint = []
	while True:
		point = getPosition()
		if point:
			print('get points ... ', point)
			updatePoint(point[0], point[1])
			if toClick:
				os.system('osascript click.scpt')


if __name__ == '__main__':
	args = sys.argv

	if len(args) > 1:
		main(True)
	else:
		main()