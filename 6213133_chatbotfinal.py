# import
from flask import Flask, request, make_response, jsonify
import os
import json
##

# LED
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
ledPin = 3
GPIO.setup(ledPin, GPIO.OUT)
#GPIO.output(ledPin, 1)

# create flask app
app = Flask(__name__)
log = app.logger

# recieve request from webhook
@app.route("/", methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
#    print(req.get('queryResult').get('parameters').get('place'))

    try:
        action = req.get('queryResult').get('intent').get('displayName')
    except AttributeError:
        return 'json error'
    # action switcher 
    #print(action)
    if action == 'TurnONLED':
        print("ON")
        res = turn_on(req)
        GPIO.output(ledPin, 1)
    elif action == 'Turn off':
        print("OFF")
        res = turn_off(req)
        GPIO.output(ledPin, 0)
    else:
        log.error('Unexpected action.')


    print('Action: ' + str(action))
    print('Response: ' + res)

    # return response
    return make_response(jsonify({'fulfillmentText': res}))

def turn_off(req):
        return 'Finish off'

def turn_on(req):
        return 'Finish on'

# run flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=int(os.environ.get('PORT','5000')))
