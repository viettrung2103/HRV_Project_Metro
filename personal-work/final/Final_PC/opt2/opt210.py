# from machine import UART, Pin, I2C, Timer
from ssd1306 import SSD1306_I2C
from fifo import Fifo


from machine import UART, Pin, I2C, Timer, ADC
from piotimer import Piotimer
import math
import time

from encoder import Isr_Fifo, Encoder
import util

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
Y_ROW_4 = Y_ROW_3 + COLUMN_SPACE + LETTER_HEIGHT

#const for led
LED1_PIN = Pin(22)
LED2_PIN = Pin(21)
LED3_PIN = Pin(20)
ON = 1 # for led, 1 is on, 0 is off
OFF = 0



#hr
t = 4 #4ms
frequency = 250
MINUTE = 60
SECOND = 1
THOUSAND = 1000
TWO = 2
test_duration = TWO  * SECOND * THOUSAND # to ms
duration = TWO * SECOND * THOUSAND

# total_time = 2 * SECOND
test_sample_size =round(test_duration / t , 0)
sample_size = round(duration / t, 0)
step = 3

age = 30
# MIN_HR = 50
# MAX_HR = 240 - age
MIN_HR = 50
MAX_HR = 150

# MIN_PULSE = 1
# MAX_PULSE = 6

MAX_ADC = 2 ** 16 -1
MIN_ADC = 0
DELTA = MAX_ADC - MIN_ADC
PERCENT = 0.12
LOWER_LIM = round(DELTA * PERCENT,0)

#for encoder
ROT_A_PIN = Pin(10)
ROT_B_PIN = Pin(11)
ROT_SW_PIN = Pin(12)
BOUNCE_TIME = 200

Y_ROW_1 = 0
Y_ROW_2 = COLUMN_SPACE + LETTER_HEIGHT
Y_ROW_3 = Y_ROW_2 + COLUMN_SPACE + LETTER_HEIGHT
Y_ROW_4 = Y_ROW_3 + COLUMN_SPACE + LETTER_HEIGHT
Y_ROW_5 = Y_ROW_4 + COLUMN_SPACE + LETTER_HEIGHT


        

class Opt210_Display:
    def __init__(self, i2c, scl_pin, sda_pin, frequency, oled_w, oled_h):
        self.i2c = I2C(i2c, scl=scl_pin, sda=sda_pin, freq=frequency)
        self.display = SSD1306_I2C(oled_w, oled_h, self.i2c)
#         self.current_flag = True
        
    def reset(self):
        self.display.fill(0)
    
    def show(self):
        text1 = "ERROR"
        text2 = "RETRY BY"
#         text3 = "BY"
        text3 = "PRESSING"
        text4 = "THE BUTTON"
        x1 = util.get_x_starting(text1)
        x2 = util.get_x_starting(text2)
        x3 = util.get_x_starting(text3)
        x4 = util.get_x_starting(text4)
#         x5 = util.get_x_starting(text5)
        self.reset()
        self.display.text(text1,x1,Y_ROW_2)
        self.display.text(text2,x2,Y_ROW_3)
        self.display.text(text3,x3,Y_ROW_4)
        self.display.text(text4,x4,Y_ROW_5)
#         self.display.text(text5,x5,Y_ROW_5)
        self.display.show()

class Opt210:
    def __init__(self,name, display, encoder, selector = None):
        self.name = name
        self.display = display
        self.encoder = encoder
        self.stop_flag = False
        self.selector = selector
        self.press = False
        
    def is_active(self):
        if self.stop_flag == False:
            return True
        else:
            return False

    
    def on(self):
        self.press = False
        self.stop_flag = False
        self.encoder.update_program(self)
        self.run()

#         self.handle_turn()

    def run(self):
        self.display.show()
        self.handle_press()

        
    def handle_press(self):
        p210_fifo = self.encoder.p210_fifo
#         print(p210_fifo)
        while p210_fifo.has_data():
            value = p210_fifo.get()
            print(f"program {self.name} press")
            if value == 1:
                self.press = True

    def off(self):
        self.stop_flag = True
        self.encoder.stop_flag = True


# adc_pin_nr = 27
# sample_size = 500 # want 250
# test_sample_size = 500
# sample_rate = 250
# hz = 20
# wait = round(1/hz,2)
# 
# samples = Isr_Fifo(sample_size,adc_pin_nr)
#         
# encoder = Encoder(ROT_A_PIN,ROT_B_PIN,ROT_SW_PIN)
#         
# opt210_display = Opt210_Display(I2C_MODE, SCL_PIN, SDA_PIN, FREQ, OLED_WIDTH, OLED_HEIGHT)
# opt210 = Opt210("210",opt210_display,encoder)
# # 
# opt210.on()


