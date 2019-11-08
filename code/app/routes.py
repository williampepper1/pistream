from flask import Flask, render_template, request, Response
from app import app
from camera_pi import Camera
import RPi.GPIO as GPIO

## SET UP
#define sensors GPIOs
button = 0
motion_detector = 0

#define actuators GPIOs
ledRed = 0
ledGreen = 0
ledYellow = 0

#initialize GPIO status
buttonSts = 0
motion_detectorSts = 0
ledRedSts = 0
ledGreenSts = 0
ledYellow = 0

#Define button and sensor pins as input
GPIO.setup(button, GPIO.IN)
GPIO.setup(motion_detector, GPIO.IN)

#define led pins as output
GPIO.setup(ledRed, GPIO.OUT)
GPIO.setup(ledYellow, GPIO.OUT)
GPIO.setup(ledGreen, GPIO.OUT)

#turn leds OFF
GPIO.output(ledRed, GPIO.LOW)
GPIO.output(ledYellow, GPIO.LOW)
GPIO.output(ledGreen, GPIO.LOW)

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True)
