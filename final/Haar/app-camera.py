from flask import Flask, render_template, Response
from cfd_web import CFD

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('stream.html')

def gen(camera):
	while True:
		frame = camera.get_frame()
		yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n'+frame+b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
	return Response(gen(CFD()), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
	app.run(host='192.168.0.125', port=8080,debug=True)


