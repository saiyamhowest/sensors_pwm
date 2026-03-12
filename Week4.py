import time
import smbus
from RPi import GPIO

GPIO.setmode(GPIO.BCM)

# RGB LED pins
red = 5
green = 6
blue = 13

# button
button = 20

GPIO.setup(red, GPIO.OUT)
GPIO.setup(green, GPIO.OUT)
GPIO.setup(blue, GPIO.OUT)

GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# PWM setup
pwm_r = GPIO.PWM(red,1000)
pwm_g = GPIO.PWM(green,1000)
pwm_b = GPIO.PWM(blue,1000)

pwm_r.start(100)
pwm_g.start(100)
pwm_b.start(100)

# I2C setup
bus = smbus.SMBus(1)
address = 0x48

# ADC channels
pot_r = 0x94   # A2
pot_g = 0xD4   # A3
pot_b = 0xA4   # A6

# max values for scaling
max_r = 1
max_g = 1
max_b = 1

system_on = True


def toggle(channel):
    global system_on
    system_on = not system_on
    print("\nSystem ON" if system_on else "\nSystem OFF")


# button interrupt
GPIO.add_event_detect(button, GPIO.FALLING, callback=toggle, bouncetime=300)

try:

    while True:

        # read ADC values
        val_r = bus.read_byte_data(address, pot_r)
        val_g = bus.read_byte_data(address, pot_g)
        val_b = bus.read_byte_data(address, pot_b)

        # update max values
        max_r = max(max_r, val_r)
        max_g = max(max_g, val_g)
        max_b = max(max_b, val_b)

        # scale to 0-255
        scaled_r = int(val_r / max_r * 255)
        scaled_g = int(val_g / max_g * 255)
        scaled_b = int(val_b / max_b * 255)

        # show values on screen
        print(f"R:{scaled_r:3}  G:{scaled_g:3}  B:{scaled_b:3}", end="\r")

        # convert to PWM (common anode LED)
        duty_r = 100 - (scaled_r / 255 * 100)
        duty_g = 100 - (scaled_g / 255 * 100)
        duty_b = 100 - (scaled_b / 255 * 100)

        if system_on:

            pwm_r.ChangeDutyCycle(duty_r)
            pwm_g.ChangeDutyCycle(duty_g)
            pwm_b.ChangeDutyCycle(duty_b)

        else:

            # LED never fully off
            pwm_r.ChangeDutyCycle(95)
            pwm_g.ChangeDutyCycle(95)
            pwm_b.ChangeDutyCycle(95)

        time.sleep(0.1)

except KeyboardInterrupt:
    pass

pwm_r.stop()
pwm_g.stop()
pwm_b.stop()
GPIO.cleanup()