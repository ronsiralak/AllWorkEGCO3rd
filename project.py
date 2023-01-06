import time
import Adafruit_ADS1x15
import RPi.GPIO as GPIO


from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.virtual import viewport, sevensegment
import lcddriver

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)

adc = Adafruit_ADS1x15.ADS1115()
lcd = lcddriver.lcd()

GAIN = 1
lcd.lcd_display_string("Hello World", 1)
while True:
	value = adc.read_adc(0,gain=GAIN)
	if (value>27000):#dark
		lcd.lcd_display_string("Have Package", 1)
    else:
        lcd.lcd_display_string("No Package", 1)
	print(value)
	time.sleep(0.1)