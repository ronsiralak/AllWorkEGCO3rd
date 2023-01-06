import time
import RPi.GPIO as GPIO
import Adafruit_ADS1x15

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.virtual import viewport, sevensegment

import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

SheetName = "Data Logger Online"
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

ButtonPin = 11
GPIO.setup(ButtonPin,GPIO.IN)

def clean():
    print("Clean")
    worksheet.clear()
    row = ["Time","Value","Status"]
    index = 1
    worksheet.insert_row(row,index)
    
def main():
    worksheet.clear()
    row = ["Time","Value","Status"]
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
        if(GPIO.input(ButtonPin)==0):
            clean()

            
        #print(value)
        if (value < 4000):
            #print("low")
            status = "Low"
        elif (value < 8000):
            #print("Medium")
            status = "Medium"
        else:
            #print("High")
            status = "High"
        now = datetime.datetime.now()
        timestamp = now.strftime("%H:%M:%S")
        Value = str(value)
        print(timestamp,Value,value,status)
        worksheet.append_row([timestamp,Value,status])
        time.sleep(1)
    


if __name__ == '__main__':
    main()



