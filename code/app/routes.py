from flask import Flask, render_template, request, Response, flash, redirect, url_for
from app import app
#from camera_pi import Camera
from camera import Camera
#import RPi.GPIO as GPIO
from flask_login import current_user, login_user
from app.models import User
from app.forms import LoginForm

## SET UP
#define sensors GPIOs
button = 0
motion_detector = 0

#define actuators GPIOs
ledRed = 0 #entrance denied
ledGreen = 0 #entrance given
ledYellow = 0 #camera recording ??

#initialize GPIO status
buttonSts = 0
motion_detectorSts = 0
ledRedSts = 0
ledGreenSts = 0
ledYellow = 0

#Define button and sensor pins as input
# GPIO.setup(button, GPIO.IN)
# GPIO.setup(motion_detector, GPIO.IN)

# #define led pins as output
# GPIO.setup(ledRed, GPIO.OUT)
# GPIO.setup(ledYellow, GPIO.OUT)
# GPIO.setup(ledGreen, GPIO.OUT)

# #turn leds OFF
# GPIO.output(ledRed, GPIO.LOW)
# GPIO.output(ledYellow, GPIO.LOW)
# GPIO.output(ledGreen, GPIO.LOW)

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        return redirect(url_for('video_feed'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('index'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('video_feed'))
    return render_template('index.html', form=form)

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
