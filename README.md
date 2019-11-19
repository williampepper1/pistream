# pistream
Video stream and surveillance application using a Raspberry Pi 4

Pistream<br>
Bill Pepper | Braden Tabisula | Eunice Kang | Taehoon Kim | Wenshi Lu<br>
IST 360 | Fall 2019<br>

<h1>Introduction</h1>
Problem description, solution description, what will be provided - deliverables
Create an internet of things system which allows a user to access a website to view a live video stream or view recorded video or images. The system will also take and save photos and/or video based on detected motion. We may also incorporate notifications like email.

<h1>Requirements</h1>
Functional & non-functional requirements
<ul>
<li>Stream to local site</li>
<li>Stream and access from the internet</li>
<li>Motion activated:</li>
<li>Notification</li>
<li>Photo</li>
<li>Video</li>
<li>Press a button to activate an actuator (i.e. Door lock!)</li>
<li>Turn motion detection on only when there are no viewers</li>
</ul>

<h1>Software/Hardware components</h1>
<ul>
<li>Raspberry Pi 4</li>
<li>Raspberry Pi Camera Module V2</li>
<li>Raspbian Operating System</li>
<li>Possible tools?</li>
    <ul>
    <li>Motion JPEG MJPEG server</li>
    <li>Flask web framework</li>
    <li>Gunicorn web server</li>
    </ul>
</ul>

<h1>Related work (similar solutions, apps/services)</h1>
<ul>
<li>https://blog.miguelgrinberg.com/post/stream-video-from-the-raspberry-pi-camera-to-web-browsers-even-on-ios-and-android</li>
<li>https://elinux.org/RPi-Cam-Web-Interface</li>
<li>https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world</li>
<li>https://gunicorn.org/</li>
<li>https://flask.palletsprojects.com/en/1.1.x/</li>
<li>https://hackaday.io/project/156072-raspberry-pi-3-as-a-web-server-using-python-iot</li>
<li>https://www.canakit.com/Media/CanaKit-Raspberry-Pi-Quick-Start-Guide-4.0.pdf</li>
<li>https://readwrite.com/2014/06/27/raspberry-pi-web-server-website-hosting/</li>
<li>https://www.instructables.com/id/Raspberry-Pi-Smart-Phone-Connected-Door-Lock/</li>
<li>https://www.hackster.io/paulfp/the-ultimate-raspberry-pi-smart-home-door-lock-3c55a0</li>
<li>https://blog.miguelgrinberg.com/post/video-streaming-with-flask</li>
<li>https://blog.miguelgrinberg.com/post/flask-video-streaming-revisited</li>
</ul>

<h1>Architecture</h1>
<h1>Description of what each team member worked on</h1>
<h1>Conclusion – limitations and future work</h1>
<h1>References</h1>

<hr>
<h1>How to run the Flask application</h1>
<p>The flask application is roughly based on <a href="https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world">this tutorial</a></p>
<p>Once you have cloned the GitHub repository, please follow these steps to run the application:</p>
<ol>
<li>Navigate to the code directory
<li>Enter "flask run"
<li>Open a web browser, enter http://127.0.0.1:5000/ into the address bar, and go!
</ol>
