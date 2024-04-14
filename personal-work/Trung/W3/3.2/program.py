import time
from machine import UART, Pin, I2C, Timer
from ssd1306 import SSD1306_I2C


I2C_MODE = 1
SCL_PIN = Pin(15)
SDA_PIN = Pin(14)
FREQ = 400000

OLED_WIDTH = 128
OLED_HEIGHT = 64
ROW_START = 0
ROW_EDGE = OLED_WIDTH - 1

HEIGHT_START = 0
HEIGHT_EDGE = OLED_HEIGHT -1

ON = 1 # for led, 1 is on, 0 is off
OFF = 0

BLANK = 0
FILLED = 1

COLUMN_SPACE = 2

class Led:
    def __init__(self,pin):
        self.led = Pin(pin, mode = Pin.OUT)
        self.status = 0 # 1 == off
        
    def is_on(self):
        if self.status == ON:
            return True
        else:
            return False
        
    def turn_on(self):
        self.led.value(on)
        
    def turn_off(self):
        self.led.value(off)
        

class Display:
    def __init__(self,i2c,scl_pin,sda_pin,frequency,oled_w, oled_h):
        self.i2c = I2C(i2c, scl=scl_pin, sda = sda_pin, freq = frequency)
        self.display = SSD1306_I2C(oled_w, oled_h, self.i2c)
        self.led_list = []
        
    def add_text(self,text):
        self.led_list.append(text)


    def show(self):
        self.display.fill(0)
        for led in self.led_list:
            print(led.fulltext())
            self.display.text(led.fulltext(), led.x_loc, led.y_loc, 1)
        self.display.show()
        
class Led_str:
    def __init__(self,text,x_loc,y_loc, led):
        self.text = text
        self.x_loc = x_loc
        self.y_loc = y_loc
        self.led = led
#         self.led_status = led.status

    def get_status_str(self):
        if self.led.is_on():
            return "ON"
        else:
            return "OFF"

    def fulltext(self):
        status_str = self.get_status_str()
        return f"{self.text} - {status_str}"


i2c = I2C (I2C_MODE, scl = SCL_PIN, sda = SDA_PIN,  freq = FREQ)
oled = SSD1306_I2C(OLED_WIDTH, OLED_HEIGHT, i2c)

LETTER_HEIGHT = 8
LETTER_WIDTH = 8
text1 = 'LED1 - OFF'
text2 = 'LED2 - OFF'
text3 = 'LED3 - OFF'
str_len = len(text1) * LETTER_WIDTH
middle_str = int(round((str_len /2),0))
x_middle = int(round(OLED_WIDTH / 2, 0)) #0 - 127
y_bottom = OLED_HEIGHT - LETTER_HEIGHT # 0 - 64
x_edge = ROW_EDGE - str_len 

x_starting = x_middle - middle_str
y_starting1 = 0
y_starting2 = COLUMN_SPACE + LETTER_HEIGHT
y_starting3 = y_starting2 + COLUMN_SPACE + LETTER_HEIGHT
color = 1
x_pre = 0



display = Display(I2C_MODE,SCL_PIN,SDA_PIN ,FREQ, OLED_WIDTH, OLED_HEIGHT)

led1 = Led(20)
led2 = Led(21)
led3 = Led(22)
led_str1 = Led_str("LED1",x_starting,y_starting1, led1)
led_str2 = Led_str("LED2",x_starting,y_starting2, led2)
led_str3 = Led_str("LED3",x_starting,y_starting3, led3)
# print("led1" ,led_string1.fulltext())
# print("led2" ,led_string2.fulltext())
# print("led3" ,led_string3.fulltext())
display.add_text(led_str1)
display.add_text(led_str2)
display.add_text(led_str3)
display.show()
