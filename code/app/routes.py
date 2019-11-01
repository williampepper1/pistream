from app import app
from flask import render_template, Response
from camera import Camera
from send_pic import attach_pic

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/video_page')
def video_page():
    return render_template('video_page.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(Camera()),
           mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/send_file')
def send_file():
    attach_pic('1.jpg')
    return render_template('video_page.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True)
