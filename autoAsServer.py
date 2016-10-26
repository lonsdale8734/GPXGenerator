from flask import Flask, jsonify, send_from_directory, request, Response
from gpxGenerator import buildGPX
import json
import os

class Point(object):
	"""docstring for Point"""
	def __init__(self, arg):
		super(Point, self).__init__()
		self.arg = arg

	def swing():

class Rote(object):

	self.back = True

			"""docstring for Rote"""
			def __init__(self, arg):
				super(Rote, self).__init__()
				self.arg = arg
						

class UserState(object):

	def __init__(self):
		super(UserState, self).__init__()
		self.setRoute([], False)

	def setPoint():
		pass

	def setRoute(self, points, back=True):
		self.points = points
		self.size = len(points)
		self.next = 0
		self.back = back

	def getNextPoint():
		if (!self.back):
			self.next = self.next % self.size
			point = self.points[self.next]
		else:
			n = self.next % (2 * self.size - 2)
			if (n >= self.size):
				n = n - 2 - n % self.size
			point = self.points[n]
		
		self.next += 1
		return point

app = Flask(__name__)
state = new UserState()

def getCurrentState():
	return state

@app.route('/point', methods = ['POST'])
def setRoute():
	prePoints = request.get_json()#[[s1,t1], [s2,t2]]
	waypoints = calculateAllPoints(prePoints)
	getCurrentState.setRoute(waypoints)
	waypoints = None
	

@app.route('/gpx', methods=['GET'])
def setPoint():
	point = getCurrentState.getNextPoint()
	return str(point[0]) + ',' + str(point[1])



@app.route('/')
def index():
	return send_from_directory('', 'index.html')

@app.route('/<path:path>')
def resource(path):
	return send_from_directory('', path)

def main():
	app.run(host = '0.0.0.0', port = 9999)

if __name__ == '__main__':
	main()