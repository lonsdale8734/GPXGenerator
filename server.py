from flask import Flask, jsonify, send_from_directory, request,Response
from gpxGenerator import buildGPX
import json

app = Flask(__name__)

@app.route('/')
def index():
	return send_from_directory('', 'index.html')

@app.route('/gpx', methods = ['POST'])
def GPX():
	prePoints = request.get_json()#[[s1,t1], [s2,t2]]
	return buildGPX(prePoints)

def display(var):
	print(type(var), var)

@app.route('/gpx', methods = ['GET'])
def GPXDownload():
	data = request.query_string.decode()
	prePoints = json.loads(data)
	gpx = buildGPX(prePoints)
	return Response(
		gpx,
		mimetype='text/xml',
		headers={'Content-disposition': 'attachment; filename=route.gpx'}
		)

@app.route('/test')
def test():
	return Response(
		"text",
		mimetype='text/plain',
		headers={'Content-disposition': 'attachment; filename=test.txt'}
		)

@app.route('/<path:path>')
def resource(path):
	return send_from_directory('', path)

def main():
	app.run(host = '0.0.0.0', port = 9999)

if __name__ == '__main__':
	main()