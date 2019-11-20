from flask import Flask, render_template, request, Response, flash, redirect, url_for
from app import app, db
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from app.forms import LoginForm, RegistrationForm, CreateUserForm

import flask_admin as admin
from flask_admin import helpers, expose
from flask_admin.contrib import sqla
from werkzeug.security import generate_password_hash, check_password_hash

import sys
import time
import threading
from app.email import sendEmail

from camera_pi import Camera
#from camera import Camera
import RPi.GPIO as GPIO

## SET UP

#pi camera
cam = Camera()

#define sensors GPIOs
button = 0
motion_detector = 0

#define actuators GPIOs
ledRed = 0 #entrance denied
ledGrn = 0 #entrance granted
ledYlw = 0 #camera is recording & processing

#initialize GPIO status
buttonSts = 0
motion_detectorSts = 0
ledRedSts = 0
ledGrnSts = 0
ledYlwSts = 0

#Define button and sensor pins as input
GPIO.cleanup()
GPIO.setwarnings(False)
GPIO.setup(button, GPIO.IN)
GPIO.setup(motion_detector, GPIO.IN)

#define led pins as output
GPIO.setup(ledRed, GPIO.OUT)
GPIO.setup(ledYlw, GPIO.OUT)
GPIO.setup(ledGrn, GPIO.OUT)

#turn leds OFF
GPIO.output(ledRed, GPIO.LOW)
GPIO.output(ledYlw, GPIO.LOW)
GPIO.output(ledGrn, GPIO.LOW)

email_update_interval = 600 #seconds
last_epoch = 0

def check_motion():
    global last_epoch
    while True:
        try:
            motion_detectorSts = GPIO.input(motion_detector)
            if motion_detectorSts == 1 and (time.time() - last_epoch)>email_update_interval:
                last_epoch = time.time()
                pic = cam.get_frame()
                # send email 
                sendEmail(pic)
        except:
            pass # what should we do?

### FLASK VIEWS

@app.route('/')
def index():
    #read sensor statuses
    ledYlwSts = GPIO.input(ledYlw)

    if ledYlwSts == 1:
        GPIO.output(ledYlw, GPIO.LOW)

    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('video_feed'))
    form = LoginForm()
    if helpers.validate_form_on_submit(form):
        user = form.get_user()
        login_user(user)
        return redirect(url_for('video_page'))
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/video_page')
@login_required
def video_page():
    GPIO.output(ledYlw, GPIO.HIGH)
    return render_template('video_page.html')

@app.route('/grant')
@login_required
def grant():
    GPIO.output(ledGrn, GPIO.HIGH)
    GPIO.output(ledYlw, GPIO.LOW)

    buttonSts = GPIO.input(button)
    motion_detectorSts = GPIO.input(motion_detector)
    ledRedSts = GPIO.input(ledRed)
    ledYlwSts = GPIO.input(ledYlw)
    ledGrnSts = GPIO.input(ledGrn)

    return render_template('video_page.html')

@app.route('/deny')
@login_required
def deny():
    GPIO.output(ledRed, GPIO.HIGH)
    GPIO.output(ledYlw, GPIO.LOW)

    buttonSts = GPIO.input(button)
    motion_detectorSts = GPIO.input(motion_detector)
    ledRedSts = GPIO.input(ledRed)
    ledYlwSts = GPIO.input(ledYlw)
    ledGrnSts = GPIO.input(ledGrn)

    return render_template('video_page.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
@login_required
def video_feed():
    return Response(gen(cam),
           mimetype='multipart/x-mixed-replace; boundary=frame')

# ADMIN VIEWS

# Create customized model view class
class MyModelView(sqla.ModelView):

    def is_accessible(self):
        return current_user.is_authenticated

class MyAdminIndexView(admin.AdminIndexView):

    @expose('/')
    def index(self):
        if not current_user.is_authenticated:
            return redirect(url_for('.login_view'))
        return super(MyAdminIndexView, self).index()

    @expose('/login/', methods=('GET', 'POST'))
    def login_view(self):
        # handle user login
        form = LoginForm(request.form)
        if helpers.validate_form_on_submit(form):
            user = form.get_user()
            login_user(user)

        if current_user.is_authenticated:
            return redirect(url_for('.index'))
        link = '<p>Don\'t have an account? <a href="' + url_for('.register_view') + '">Click here to register.</a></p>'
        self._template_args['form'] = form
        self._template_args['link'] = link
        return super(MyAdminIndexView, self).index()

    @expose('/register/', methods=('GET', 'POST'))
    def register_view(self):
        form = RegistrationForm(request.form)
        if helpers.validate_form_on_submit(form):
            user = User()

            form.populate_obj(user)
            # we hash the users password to avoid saving it as plaintext in the db,
            # remove to use plain text:
            user.password = generate_password_hash(form.password.data)

            db.session.add(user)
            db.session.commit()

            login_user(user)
            return redirect(url_for('.index'))
        link = '<p>Already have an account? <a href="' + url_for('.login_view') + '">Click here to log in.</a></p>'
        self._template_args['form'] = form
        self._template_args['link'] = link
        return super(MyAdminIndexView, self).index()

    @expose('/logout/')
    def logout_view(self):
        logout_user()
        return redirect(url_for('.index'))

class UserAdminView(sqla.ModelView):
    column_exclude_list = ['password_hash', ]
    form = CreateUserForm

if __name__ == '__main__':
    t = threading.Thread(target=check_motion, args=())
    t.daemon = True
    t.start()
    app.run(host='0.0.0.0', debug=True, threaded=True)
