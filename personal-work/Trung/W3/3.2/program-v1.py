import time
from machine import UART, Pin, I2C, Timer
from ssd1306 import SSD1306_I2C
from fifo import Fifo
import micropython
micropython.alloc_emergency_exception_buf(200)


# const for display
I2C_MODE = 1
SCL_PIN = Pin(15)
SDA_PIN = Pin(14)
FREQ = 400000

OLED_WIDTH = 128
OLED_HEIGHT = 64
ROW_START = 0
ROW_EDGE = OLED_WIDTH - 1 #127
HEIGHT_START = 0
HEIGHT_EDGE = OLED_HEIGHT -1 #63

BLANK = 0
FILLED = 1
COLUMN_SPACE = 2
LETTER_HEIGHT = 8
LETTER_WIDTH = 8
Y_ROW_1 = 0
Y_ROW_2 = COLUMN_SPACE + LETTER_HEIGHT
Y_ROW_3 = Y_ROW_2 + COLUMN_SPACE + LETTER_HEIGHT

#const for led
ON = 1 # for led, 1 is on, 0 is off
OFF = 0

def get_x_starting(text):
    str_len = len(text) * LETTER_WIDTH
    middle_str = int(round((str_len /2),0))
    x_middle = int(round(OLED_WIDTH / 2, 0)) #0 - 127
    x_starting = x_middle - middle_str
    return x_starting

class Encoder:
    def __init__ (self, rot_a, rot_b):
        self.a = Pin(rot_a, mode = Pin.IN, pull = Pin.PULL_UP)
        self.b = Pin(rot_b, mode = Pin.IN, pull = Pin.PULL_UP)
        self.turn_fifo = Fifo(30, typecode = "i")
        self.a.irq (handler = self.handler, trigger = Pin.IRQ_RISING, hard = True)
    
    def handler(self,pin):
        #when knob is rotates, check state of b, if b is 1, turn clockwise, if b is 0, turn anti clockwise
        if self.b():
            self.turn_fifo.put(1)
        else:
            self.turn_fifo.put(-1)
            

class Led:
    def __init__(self,pin):
        self.led = Pin(pin, mode = Pin.OUT)
        self.status = 1 # 1 == on
        
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
        self.led_str_list = []
        
        
    def add_text(self,text):
        self.led_str_list.append(text)
        
    def reset(self):
        self.display.fill(0)


    def show_result(self,select):
        self.reset()
        for index, led in enumerate(self.led_str_list):

            if select.current_pos == index:

                self.display.text(select.sel_str, select.x_loc, select.y_loc, 1)
            else:

                self.display.text(led.fulltext(), led.x_loc, led.y_loc, 1)
        self.display.show()
        
        
    
        
class Led_str:
    def __init__(self,text,x_loc,y_loc, led):
        self.text = text
        self.x_loc = x_loc
        self.y_loc = y_loc
        self.led = led
#         self.led_status = led.status

    def get_x(self):
        return self.x_loc
    
    def get_y(self):
        return self.y_loc

    def get_status_str(self):
        if self.led.is_on():
            return "ON"
        else:
            return "OFF"

    def fulltext(self):
        status_str = self.get_status_str()
        return f"{self.text} - {status_str}"
    
class Selection:
    def __init__(self,x_loc,y_loc):
        self.x_loc = x_loc
        self.y_loc = y_loc
#         self.color = 1
#         self.color_text = 0
        self.sel_str = ""
        self.current_pos = 2
        
    def get_select_str(self,led_str):
        return f"[ {led_str.fulltext()} ]"
    
#     def get_select_x_loc(self,led_str):
#         return led_str.


class Program:
    def __init__(self,display,encoder,led1,led2,led3,select):
        self.display = display
        self.encoder = encoder
        self.led1 = led1
        self.led2 = led2
        self.led3 = led3
        self.select = select
        
    def get_box_info(self):
        current_led_str = self.display.led_str_list[self.select.current_pos]
        self.select.sel_str = self.select.get_select_str(current_led_str)
        self.select.x_loc = get_x_starting(self.select.sel_str)

        self.select.y_loc = current_led_str.get_y()
        
    def run(self):
        while True:
            self.get_box_info()
            self.display.show_result(self.select)
            while self.encoder.turn_fifo.has_data():
                print(encoder.turn_fifo.get())




text1 = 'LED1 - OFF'
text2 = 'LED2 - OFF'
text3 = 'LED3 - OFF'



x_starting = get_x_starting(text1)
y_starting1 = Y_ROW_1
y_starting2 = Y_ROW_2
y_starting3 = Y_ROW_3
# color = 1
# x_pre = 0



display = Display(I2C_MODE,SCL_PIN,SDA_PIN ,FREQ, OLED_WIDTH, OLED_HEIGHT)

led1 = Led(20)
led2 = Led(21)
led3 = Led(22)
encoder = Encoder(10,11)
select = Selection(0,0)


program = Program(display, encoder, led1, led2, led3, select)

led_str1 = Led_str("LED1",x_starting,y_starting1, led1)
led_str2 = Led_str("LED2",x_starting,y_starting2, led2)
led_str3 = Led_str("LED3",x_starting,y_starting3, led3)
# print("led1" ,led_string1.fulltext())
# print("led2" ,led_string2.fulltext())
# print("led3" ,led_string3.fulltext())
display.add_text(led_str1)
display.add_text(led_str2)
display.add_text(led_str3)





while True:
#     display.show_resul()
#     while rot.turn_fifo.has_data():
#         print(rot.turn_fifo.get())
    program.run()

