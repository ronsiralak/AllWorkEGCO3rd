import time
import Adafruit_ADS1x15
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)
p = GPIO.PWM(11, 100)
p.start(0)

adc = Adafruit_ADS1x15.ADS1115()

GAIN = 1
while True:
	value = adc.read_adc(0,gain=GAIN)
	if value<0:
		value=0
	duty=(value*100)/40000
	print(value,duty)
	p.ChangeDutyCycle(duty)
	time.sleep(0.1)
