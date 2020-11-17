import lcd
from mfrc522 import SimpleMFRC522
import RPi.GPIO as gpio
import time
import requests

class Handler:
	def __init__(self):
		self.gpio = gpio
		self.gpio.setmode(gpio.BCM)
		self.gpio.setwarnings(False)
		self.gpio.cleanup()
		self.reader = SimpleMFRC522()
		self.lcd = lcd
		self.lcd.lcd_init()
	def read_rfid(self):
		try:
			id_no,info = self.reader.read()
			if info.find('-')<0:
				print('Scan Again..')
				return None
			info = info.split('-')
			item,price = info[0],int(info[1])
			response = [id_no,item,price]
			return response
		except:
			print('Scan Again...')
	def write_lcd(self,line,message):
		if line == 1:
			self.lcd.lcd_byte(self.lcd.LCD_LINE_1,self.lcd.LCD_CMD)			
		elif line ==2:
			self.lcd.lcd_byte(self.lcd.LCD_LINE_2,self.lcd.LCD_CMD)
		self.lcd.lcd_string(message,1)

	def clear_lcd(self):
		self.lcd.lcd_byte(self.lcd.LCD_LINE_1,self.lcd.LCD_CMD)
		self.lcd.lcd_string(" ",1)
		self.lcd.lcd_byte(self.lcd.LCD_LINE_2,self.lcd.LCD_CMD)
		self.lcd.lcd_string(" ",1)
	def button_pressed(self,channel):
		print('Pressed')
item_list = {}
handler = Handler()
time.sleep(1)
handler.clear_lcd()
time.sleep(1)
total = 0
url = "http://localhost:1234/update"
while(True):
	if total == 0:
		handler.write_lcd(1," Welcome to")
		handler.write_lcd(2,"Smart Shopping")
	else:
		handler.write_lcd(1,"Total Items :"+str(len(item_list.keys())))
		handler.write_lcd(2,"Price : "+str(total))		
	response = handler.read_rfid()
	if response == None:
		continue
	if response[0] in item_list.keys():
		item_list.pop(response[0])
		handler.write_lcd(1,response[1]+" removed")
	else:
		item_list[response[0]] = [response[1],response[2]];
		handler.write_lcd(1,response[1]+" added")
	handler.write_lcd(2,"Price : "+str(response[2]))
	time.sleep(2)
	total = 0 
	for i in item_list.keys():
		total += item_list[i][1]
	try:
		response = requests.get(url,params=item_list)
		print(response)
	except:
		print('Connection Error..')
		continue

