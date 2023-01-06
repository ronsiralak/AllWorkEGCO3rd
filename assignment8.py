import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
ButtonPin = 11
GPIO.setup(ButtonPin,GPIO.IN)
GPIO.setup(3,GPIO.OUT)
GPIO.output(3,GPIO.HIGH)

import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

SheetName = "Lab8"
GSheet_OAUTH_JSON = "data-logger-online-345608-d616f7cab9d4.json"
scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/drive"]

credentials = ServiceAccountCredentials.from_json_keyfile_name(GSheet_OAUTH_JSON, scope)
client = gspread.authorize(credentials)
worksheet = client.open(SheetName).sheet1

worksheet.clear()
row = ["Time","Status"]
index = 1
worksheet.insert_row(row,index)

now = datetime.datetime.now()
timestamp = now.strftime("%H:%M:%S")
worksheet.update('A2:B2',[[timestamp,"ON"]])

status = 1
Status = ""
        
while(True):
    if(GPIO.input(ButtonPin)==0):
        if(status == 1):
            status = 0
            Status = "OFF"
            GPIO.output(3,GPIO.LOW)
            
        else:
            status = 1
            Status = "ON"
            GPIO.output(3,GPIO.HIGH)
        print("click",status)
        now = datetime.datetime.now()
        timestamp = now.strftime("%H:%M:%S")
        worksheet.update('A2:B2',[[timestamp,Status]])
