import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqtt # pip3 install paho-mqtt
import json
import random
import os
from flask import Flask, request, make_response, jsonify
myData = { "ID" : 123, "value" : 0}

# Initialize Netpie information
NETPIE_HOST = "broker.netpie.io"
CLIENT_ID = "e851b5e5-b2e6-4e26-acd5-a887937d008f" # YOUR CLIENT ID
DEVICE_TOKEN = "FA9nn4nyya3X6E6Nwf35qzBcxfNfGLVG" # YOUR TOKEN

#Board setup
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GAIN=1
# Function to react with NETPIE
def on_connect(client, userdata, flags, rc):
    print("Result from connect : {}".format(mqtt.connack_string(rc)))
    client.subscribe("@shadow/data/updated")

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribe successful")

def on_message(client, userdata, msg):
    #print(str(msg.payload))
    data = str(msg.payload).split(",")
    #print(data)
    data_split = data[1].split("{")[1].split(":")
    data_split2 = data[2].split(":")

    # print(data_split)
    # print(data_split2)
    key = data_split[0].split('"')[1]
    # key2 = data_split2[0].split('"')[1]
    # print(key)
    value = data_split[1].split('}')[0]
    # value2 = data_split2[1].split('}')[0]
    # print(value)
    # print(value2)
    if value[0] == '"':
        value = value.split('"')[1]
    
    myData[key] = value
  
    # print(key,value)
    #nvalue = value
    #print("nvalue " +nvalue)
    #if(nvalue =="ON"):
        #GPIO.output(11,GPIO.HIGH)
    #if(nvalue == "OFF"):
        #GPIO.output(11,GPIO.LOW)
    # print(key2,value2)


#Connecting to NETPIE
client = mqtt.Client(protocol=mqtt.MQTTv311,client_id=CLIENT_ID, clean_session=True)
client.username_pw_set(DEVICE_TOKEN)
client.on_connect = on_connect
client.on_message = on_message
client.connect(NETPIE_HOST, 1883)
client.loop_start()

value = 0
import time
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

SheetName = "Data Logger Online"
GSheet_OAUTH_JSON = "data-logger-online-345608-d616f7cab9d4.json"
scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/drive"]

credentials = ServiceAccountCredentials.from_json_keyfile_name(GSheet_OAUTH_JSON, scope)
clientsheet = gspread.authorize(credentials)
worksheet = clientsheet.open(SheetName).sheet1

worksheet.clear()
row = ["AQI","PM2.5","Time"]
index = 1
worksheet.insert_row(row,index)

while True:
	
    aqi = random.randint(0,100)
    pm25 = random.randint(0,250)
    myData['value'] = pm25
    myData['ID'] = aqi
    now = datetime.datetime.now()
    timestamp = now.strftime("%H:%M:%S")
    worksheet.append_row([aqi,pm25, timestamp])
    #send myData (in JSON from) to NETPIE2020 shadow
    client.publish("@shadow/data/update",json.dumps({"data": myData}), 1)

    time.sleep(3)
