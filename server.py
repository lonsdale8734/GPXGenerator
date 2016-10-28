from flask import Flask, jsonify, send_from_directory, request, Response
import PointGenerator
import json


class UserState(object):

	__toWalkAround = False
	__routeStack = []
	__currentRoute = None
	__speed = 1# 1 - 10
	
	def __init__(self):
		super(UserState, self).__init__()

	def addRoute(self, route):
		self.__routeStack.append(route)

	def removeRoute(self):
		del self.__routeStack[-1]

	def clearRoute(self):
		__routeStack = [] # del [:]

	def setSpeed(self, speed):
		self.__speed = speed

	def getNextPoint(self):
		if self.__routeStack:
			return self.__routeStack[-1].getNextPoint(self.__speed)
		else:
			print('no route')
			return []

	def getCurrentPoint(self):
		return self.__routeStack[-1].getCurrentPoint()

	def pause(self):
		return self.__routeStack[-1].pause()

	def start(self):
		return self.__routeStack[-1].start()


state = UserState()
def getCurrentState():
	return state



app = Flask(__name__)

@app.route('/speed', methods = ['POST'])
def setSpeed():
	speed = request.get_json()#str
	print('set speed to ', speed)
	getCurrentState().setSpeed(float(speed))
	return 'ok'

@app.route('/route', methods = ['POST'])
def setRoute():
	print('add new route')
	breakPoints = request.get_json()#[[s1,t1], [s2,t2]]
	route = PointGenerator.LineRoute(breakPoints)
	getCurrentState().addRoute(route)
	return 'ok'

@app.route('/scan', methods = ['POST'])
def setCycleRoute():
	print('start to scan ...')
	point = getCurrentState().getCurrentPoint()
	route = PointGenerator.getCycleRoute(point)
	getCurrentState().addRoute(route)
	return 'ok'

@app.route('/pop')
def popRoute():
	getCurrentState().removeRoute()
	return 'ok'

@app.route('/pause')
def pause():
	getCurrentState().pause()
	return 'ok'

@app.route('/start')
def start():
	getCurrentState().start()
	return 'ok'

@app.route('/next')
def getNextPoint():
	print('fetch next point')
	nextPoint = getCurrentState().getNextPoint()
	print('fetch next point', nextPoint, type(nextPoint))
	return str(nextPoint)

@app.route('/point', methods = ['GET'])
def getCurrentPoint():
	print('fetch current point')
	return str(getCurrentState().getCurrentPoint())


@app.route('/')
def index():
	return send_from_directory('front', 'index.html')

@app.route('/<path:path>')
def resource(path):
	return send_from_directory('front', path)

def main():
	app.run(host = '0.0.0.0', port = 9999)

if __name__ == '__main__':
	main()