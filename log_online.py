import time
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

SheetName = "Data Logger Online"
GSheet_OAUTH_JSON = "datalog-345606-402bed01f104.json"
scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/drive"]

credentials = ServiceAccountCredentials.from_json_keyfile_name(GSheet_OAUTH_JSON, scope)
client = gspread.authorize(credentials)
worksheet = client.open(SheetName).sheet1

row = ["Date","Time"]
index = 1
worksheet.insert_row(row,index)

while True:
	now = datetime.datetime.now()
	Date = now.strftime("%d/%m/%Y")
	timestamp = now.strftime("%H:%M:%S")
	try:
		worksheet.append_row([Date, timestamp])
	except Exception as ex:
		print("Google sheet login failed with error:",ex)
	time.sleep(2)
