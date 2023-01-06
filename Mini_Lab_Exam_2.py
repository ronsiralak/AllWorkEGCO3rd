import time
import RPi.GPIO as GPIO
import Adafruit_ADS1x15

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.virtual import viewport, sevensegment

import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

import lcddriver

import paho.mqtt.client as mqtt # pip3 install paho-mqtt
import json

# Initialize Netpie information
NETPIE_HOST = "broker.netpie.io"
CLIENT_ID = "e851b5e5-b2e6-4e26-acd5-a887937d008f" # YOUR CLIENT ID
DEVICE_TOKEN = "FA9nn4nyya3X6E6Nwf35qzBcxfNfGLVG" # YOUR TOKEN

SheetName = "LabExam2"
GSheet_OAUTH_JSON = "data-logger-online-345608-d616f7cab9d4.json"
scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/drive"]

credentials = ServiceAccountCredentials.from_json_keyfile_name(GSheet_OAUTH_JSON, scope)
client = gspread.authorize(credentials)
worksheet = client.open(SheetName).sheet1

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)

adc = Adafruit_ADS1x15.ADS1115()
GAIN = 1
serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, cascaded=1)
seg = sevensegment(device)
    
lcd = lcddriver.lcd()

myData = { "ID" : 123, "value" : 0}

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
    nvalue = value
    print("nvalue " +nvalue)
    if(nvalue =="HELLO"):
        lcd.lcd_display_string("Hello", 1)
        lcd.lcd_display_string(timestamp, 2)
    # print(key2,value2)



#Connecting to NETPIE
client = mqtt.Client(protocol=mqtt.MQTTv311,client_id=CLIENT_ID, clean_session=True)
client.username_pw_set(DEVICE_TOKEN)
client.on_connect = on_connect
client.on_message = on_message
client.connect(NETPIE_HOST, 1883)
client.loop_start()

worksheet.clear()
row = ["Time","Value"]
index = 1
worksheet.insert_row(row,index)
serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, cascaded=1)
while True:
    value = adc.read_adc(0, gain=GAIN)
    if (value < 0):
        value = 0
    status = ""
    Value = ""
    if(value > 5000):
        GPIO.output(11,GPIO.HIGH)
    else:
        GPIO.output(11,GPIO.LOW)

    #print(value)
    now = datetime.datetime.now()
    timestamp = now.strftime("%H:%M:%S")
    Value = str(value)
    seg.text = Value
    print(timestamp,Value,value,status)
    worksheet.append_row([timestamp,Value])
    myData['value'] = value 
    myData['ID'] = timestamp
    #send myData (in JSON from) to NETPIE2020 shadow
    client.publish("@shadow/data/update",json.dumps({"data": myData}), 1)
    time.sleep(3)
