from math import radians, cos, sin, asin, sqrt, ceil
import math

R = 6371 * 1000

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
    return c * R

def deltaDegree(distance):
	return distance * 180 / (math.pi * R)

#include start point, exclude stop point
def calculateStepPoints(startPoint, stopPoint, stepDistance=1.5):
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

def calculateAllPoints(prePoints, stepDistance=1.5):
	waypoints = []
	for i in range(len(prePoints) - 1):
		stepPoints = calculateStepPoints(prePoints[i], prePoints[i + 1], stepDistance)
		waypoints.extend(stepPoints)
	waypoints.append(prePoints[-1])
	return waypoints

# n = 3:
# * * * * *
# * * * * *
# * * * * *
# * * * * *
# * * * * *
def calculateRoundPoints(level):
	def getPointsInLevel(n):
	#from most top left point
		points = []
		for i in range(1-n, n-1, 1):
			points.append((i, n-1))

		for i in range(n-1, 1-n, -1):
			points.append((n-1, i))

		for i in range(n-1, 1-n, -1):
			points.append((i, 1-n))

		for i in range(1-n, n-1, 1):
			points.append((1-n, i))
		return points or [(0, 0)]

	points = []
	for i in range(level, 0, -1):
		points.extend(getPointsInLevel(i))
	return points[-1:0:-1]


class LineRoute(object):
	"""docstring for LineRoute"""

	__stopped = False
	__isBacking = False
	__backDirect = False

	def __init__(self, breakPoints, isDirect=False):
		super(LineRoute, self).__init__()
		breakPoints = breakPoints[:]
		self.__breakPoints = breakPoints
		self.__wayPoints = calculateAllPoints(breakPoints)
		self.__directPoints = calculateStepPoints(breakPoints[0], breakPoints[-1])

		self.__pointIndex = 0
		self.__currentPoint = breakPoints[0]
		self.__backDirect = isDirect

	def getNextPoint(self, speed):
		if not self.__stopped:
			self.__currentPoint = self.getNextPoint(speed)
		return self.__currentPoint

	def getCurrentPoint(self):
		return self.__currentPoint

	def pause(self):
		self.__stopped = True

	def start(self):
		self.__stopped = False

	def setLocation(point):
		self.__currentPoint = point[:]

	def __scaleSpeed(self, speed):
		speed = math.round(speed)
		if speed < 0:
			return 0
		elif speed > 10:
			return 10
		else:
			return speed

	def __getNextForwardPointIndex(self, speed):
		lastIndex = len(self.__wayPoints) - 1
		nextIndex = self.__pointIndex + speed

		if nextIndex >= lastIndex:
			nextIndex = lastIndex
			self.__isBacking = True

		return nextIndex

	def __getNextBackPointIndex(self, speed):
		firstIndex = 0
		nextIndex = self.__pointIndex - speed

		if nextIndex <= firstIndex:
			nextIndex = firstIndex
			self.__isBacking = False

		return nextIndex

	def __getNextForwardPoint(self, speed):
		nextIndex = self.__getNextBackPointIndex(speed)
		return self.__wayPoints[nextIndex]

	def __getNextBackPoint(self, speed):
		nextIndex = self.__getNextBackPointIndex(speed)

		if self.__backDirect:
			return self.__directPoints[nextIndex]
		else:
			return self.__wayPoints[nextIndex]

	def __getNextPoint(self, speed):
		speed = self.__scaleSpeed(speed)

		lastIndex = len(self.__wayPoints) - 1
		if self.__isBacking:
			return self.__getNextBackPoint(speed)
		else:
			return self.__getNextForwardPoint(speed)

def getCycleRoute(point):
	unit = deltaDegree(80) #meter
	breakPoints = []
	for item in calculateRoundPoints(3);
		breakPoints.append(item[0]*unit + point[0],
			item[1]*unit + point[1])

	return LineRoute(breakPoints, True)

def testSpeed():
	pass

if __name__ == '__main__':
	print(calculateRoundPoints(2))