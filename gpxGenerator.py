
def generatePointGPX(lat, lon):
	return '<wpt lat="{lat}" lon="{lon}"></wpt>'\
		.format(lat=lat, lon=lon)

def generateGPX(waypoints):
	gpx = """<?xml version="1.0" encoding="UTF-8" ?>
<gpx version="1.1">
"""

	for point in waypoints:
		gpx += '\t' + generatePointGPX(*point) + '\n'

	for point in reversed(waypoints):
		gpx += '\t' + generatePointGPX(*point) + '\n'

	gpx += '</gpx>'

	return gpx


from math import radians, cos, sin, asin, sqrt, ceil

def distance(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 #km
    return c * r * 1000

#include start point, exclude stop point
def calculatePoints(startPoint, stopPoint, stepDistance):
	d = distance(*startPoint, *stopPoint)
	n = ceil(d / stepDistance)

	stepLat = (stopPoint[0] - startPoint[0]) / n
	stepLon = (stopPoint[1] - startPoint[1]) / n

	points = []
	for i in range(n):
		lat = startPoint[0] + i * stepLat
		lon = startPoint[1] + i * stepLon
		points.append((lat, lon))
	return points



def buildGPX(prePoints, stepDistance=2):
	waypoints = []
	for i in range(len(prePoints) - 1):
		stepPoints = calculatePoints(prePoints[i], prePoints[i + 1], stepDistance)
		waypoints.extend(stepPoints)
	waypoints.append(prePoints[-1])

	return generateGPX(waypoints)



if __name__ == '__main__':
	prePoints = [
		(1.2982572, 103.7878278),
		(1.2991791, 103.7857474),
	]
	with open('point.gpx', 'w') as writer:
		writer.write(buildGPX(prePoints))