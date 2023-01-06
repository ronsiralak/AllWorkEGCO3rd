import time
import RPi.GPIO as GPIO
import Adafruit_ADS1x15
from datetime import datetime
from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.virtual import viewport, sevensegment

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
buttonPin =5

GPIO.setup(buttonPin,GPIO.IN,pull_up_down = GPIO.PUD_UP)
count = 0
seg = None
def button_pressed_callback(channel):
    global count
    count =count + 1
    print(count)
    seg.text = str(count)


def main():
    # create seven segment device
    global seg
    serial = spi(port=0, device=0, gpio=noop())
    device = max7219(serial, cascaded=1)
    seg = sevensegment(device)
    seg.text = str(0)
    GPIO.add_event_detect(buttonPin, GPIO.FALLING, callback=button_pressed_callback, bouncetime=200)
    try:
        message = input("press enter to quit")
        GPIO.cleanup()
    except:
        print("END")




if __name__ == '__main__':
    main()
