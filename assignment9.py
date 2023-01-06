from flask import Flask,render_template,jsonify,request
import datetime
import RPi.GPIO as GPIO
import Adafruit_ADS1x15

app = Flask(__name__)
import Adafruit_ADS1x15
adc = Adafruit_ADS1x15.ADS1115()

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

GAIN = 1
normal = 0
prev = 0

@app.route('/')
def index():
    print("Startweb")
    return render_template('index.html')


@app.route('/<action>')
def Control(action):
    print("Control")
    global normal
    global prev
    if prev == 1:
        normal = 0
        prev = 0
        print("Normal")
    elif prev == 0:
        normal = 1
        prev = 1
        print("Not normal")
    return jsonify(status = action)
        
@app.route('/sensorup')
def updateSensor():
    global normal
    adc = Adafruit_ADS1x15.ADS1115()
    print("Update")
    value =adc.read_adc(0,gain=1)
    if(value < 0):
        value = 0
    print("Value = "+str(value))
    
        
    if(normal ==1):
        value = (value*100)/15000
        strval = '<0 - 100>' + str(value)
    else:
        strval = '<0 - 15000>' + str(value)
    return jsonify(sensorupdate=strval)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port = 5000)