import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqtt # pip3 install paho-mqtt
import json
import random
import Adafruit_ADS1x15

myData = { "ID" : 123, "value" : 0}

# Initialize Netpie information
NETPIE_HOST = "broker.netpie.io"
CLIENT_ID = "719cb8ec-507d-47aa-8c48-7943c041699c" # YOUR CLIENT ID
DEVICE_TOKEN = "6TABWTdrUkKVbgC7ogkQEegUywJU1ca2" # YOUR TOKEN

#Board setup
adc = Adafruit_ADS1x15.ADS1115()
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)
GPIO.output(11,GPIO.LOW)
GAIN=1
# Function to react with NETPIE
def on_connect(client, userdata, flags, rc):
    print("Result from connect : {}".format(mqtt.connack_string(rc)))
    client.subscribe("@shadow/data/updated")

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribe successful")

def on_message(client, userdata, msg):
    # print(str(msg.payload))
    data = str(msg.payload).split(",")
    # print(data)
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
    print(nvalue)
    if(nvalue =="ON"):
        GPIO.output(11,GPIO.HIGH)
    if(nvalue == "OFF"):
        GPIO.output(11,GPIO.LOW)
    # print(key2,value2)


#Connecting to NETPIE
client = mqtt.Client(protocol=mqtt.MQTTv311,client_id=CLIENT_ID, clean_session=True)
client.username_pw_set(DEVICE_TOKEN)
client.on_connect = on_connect
client.on_message = on_message
client.connect(NETPIE_HOST, 1883)
client.loop_start()

value = 0
try :
    while True:
        value =adc.read_adc(0,gain=GAIN)
        myData['value'] = value 
        myData['ID'] = "123"

        #send myData (in JSON from) to NETPIE2020 shadow
        client.publish("@shadow/data/update",json.dumps({"data": myData}), 1)
        time.sleep(5)

except KeyboardInterrupt:
    print('Disconnecting successful')
    GPIO.cleanup()
