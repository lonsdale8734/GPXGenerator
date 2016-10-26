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
		return self.__routeStack[-1].getNextPoint(self.__speed)

	def getCurrentPoint(self):
		return self.__routeStack[-1].getCurrentPoint()


state = new UserState()
def getCurrentState():
	return state



app = Flask(__name__)

@app.route('/route', methods = ['POST'])
def setRoute():
	breakPoints = request.get_json()#[[s1,t1], [s2,t2]]
	route = PointGenerator.LineRoute(breakPoints)
	getCurrentState.addRoute(route)

@app.route('/cycle', methods = ['POST'])
def setCycleRoute():
	breakPoints = request.get_json()#[[s1,t1], [s2,t2]]
	route = PointGenerator.getCycleRoute(breakPoints[0])
	getCurrentState.addRoute(route)

@app.route('/pause')
def pause():
	pass

@app.route('/start')
def start():
	pass

@app.route('/next')
def getNextPoint():
	return str(getCurrentState.getNextPoint())

@app.route('/point', methods = ['GET'])
def getCurrentPoint():
	return str(getCurrentState.getCurrentPoint())


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