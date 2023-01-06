import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(5,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(7,GPIO.OUT)
global state
state = 0
GPIO.output(7,state)

def button_pressed_callback(channel):
    global state
    print("Pressed")
    if(state==0):
        state = 1
    else:
        state = 0
    GPIO.output(7,state)
GPIO.add_event_detect(5,GPIO.FALLING,callback=button_pressed_callback,bouncetime=200)

try:
    message = input("Press Enter to quit")
    GPIO.cleanup()
except:
    print("END")