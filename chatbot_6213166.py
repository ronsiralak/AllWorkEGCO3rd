# import
import RPi.GPIO as GPIO
import time
import json
import random
import gspread
from flask import Flask, request, make_response, jsonify
import os
from oauth2client.service_account import ServiceAccountCredentials
import datetime
myData = { "ID" : 123, "value" : 0}

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(3,GPIO.OUT)

#initialize google sheet
SheetName = "Data Logger Online"
GSheet_OAUTH_JSON = "diesel-ellipse-345606-40b8f27bafca.json"
scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/drive"]

credentials = ServiceAccountCredentials.from_json_keyfile_name(GSheet_OAUTH_JSON, scope)
client = gspread.authorize(credentials)
worksheet = client.open(SheetName).sheet1

# create flask app
app = Flask(__name__)
log = app.logger
list_of_lists = []
# recieve request from webhook
@app.route("/", methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    # print(req.get('queryResult').get('parameters').get('status'))
    status = req.get('queryResult').get('parameters').get('status')[0]
    status =status.lower()
    try:
        action = req.get('queryResult').get('intent').get('displayName')
    except AttributeError:
        return 'json error'
    # read data from google sheet 
    global list_of_lists
    list_of_lists = worksheet.get_all_values()
 
    res = ""
    print(status)
    if action == 'AQI':
        if(status == "current"):
            res = current_value(status,"AQI")
        else:
            res = search_value(status,"AQI")
    elif action == 'PM':
        if(status == "current"):
            res = current_value(status,"PM")
        else:
            res = search_value(status,"PM")
    elif action == 'both':
        if(status == "current"):
            res = current_value(status,"both")
        else:
            res = search_value(status,"both")
    else:
        log.error('Unexpected action.')
        


    return make_response(jsonify({'fulfillmentText': res}))
def current_value(status,param):
    global list_of_lists
    last = len(list_of_lists)
    value = list_of_lists.pop(last-1)
    word = ""
    if(param == "AQI"):
        word =  " AQI : "+ str(value[1])
    elif(param == "PM"):
        word =  " PM: "+ str(value[2])
    elif(param == "both"):
        word =  " AQI and PM : " + str(value[1]) + " : " + str(value[2]) 
    
    return "Time " + str(value[0])  + ": " + word

def search_value(status,param):
    global list_of_lists
    text = "not found"
    word = ""
    for i in list_of_lists[1:]:
        print(status + " : " + str(i[0]))
        if(status== str(i[0])):
            text = "Timestamp : " + str(i[0]) 
            if(param == "AQI"):
                word =  " AQI : "+ str(i[1])
            elif(param == "PM"):
                word =  " PM: "+ str(i[2])
            elif(param == "both"):
                word =  " AQI and PM : " + str(i[1]) + " : " + str(i[2]) 
            break
    text += word 
    return text


# run flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=int(os.environ.get('PORT','5000')))
