import RPi.GPIO as GPIO
import time

pir_sensor = 11
led = 7

GPIO.setmode(GPIO.BOARD)

GPIO.setup(led, GPIO.OUT)
GPIO.setup(pir_sensor, GPIO.IN)

current_state = 0

try:
        while True:
                time.sleep(0.1)
                current_state = GPIO.input(pir_sensor)
                if current_state == 1:
                        print("Motion Detected")
                        GPIO.output(led, True)
                        time.sleep(2)
                        GPIO.output(led, False)
                        time.sleep(4)
except KeyboardInterrupt:
        pass
finally:
        GPIO.cleanup()

