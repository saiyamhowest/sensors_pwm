import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

led=17
GPIO.setup(led,GPIO.OUT)

pwm = GPIO.PWM(led , 1000)

pwm.start(0)

try:
    while True:
        pwm.ChangeDutyCycle(10)
        time.sleep(0.5)

        pwm.ChangeDutyCycle(0)
        time.sleep(0.5)

        pwm.ChangeDutyCycle(100)
        time.sleep(0.5)

        pwm.ChangeDutyCycle(0)
        time.sleep(0.5)

except KeyboardInterrupt:
    pwm.stop()
    GPIO.cleanup()