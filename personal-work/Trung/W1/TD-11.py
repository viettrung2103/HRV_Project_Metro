import time
from machine import UART, Pin, I2C, Timer
from ssd1306 import SSD1306_I2C

LEFT_PIN = 9
RIGHT_PIN= 7

I2C_MODE = 1
SCL_PIN = Pin(15)
SDA_PIN = Pin(14)
FREQ = 400000

OLED_WIDTH = 128
OLED_HEIGHT = 64

button = Pin(9, Pin.IN, Pin.PULL_UP)

left_button = Pin(LEFT_PIN, Pin.IN, Pin.PULL_UP)
right_button = Pin(RIGHT_PIN, Pin.IN, Pin.PULL_UP)

i2c = I2C (I2C_TYPE, scl = SCL_PIN, sda = SDA_PIN,  freq = FREQ)
oled = SSD1306_I2C(OLED_WIDTH, OLED_HEIGHT, i2c)

letter_height = 8
letter_width = 8
row_starting = 0
row_edge = OLED_WIDTH - 1

height_starting = 0
height_edge = OLED_HEIGHT -1




#starting position
ufo = 'trung'
str_len = len(ufo) * letter_width
middle_str = int(round((str_len /2),0))
x_middle = int(round(OLED_WIDTH / 2, 0)) #0 - 127
y_bottom = OLED_HEIGHT - letter_height # 0 - 64
x_edge = row_edge - str_len 

x = x_middle - middle_str
y = y_bottom
color = 1
x_pre = 0

def left_pressed():
    return left_button == 0

def right_pressed():
    return right_button == 0

oled.fill(0)
oled.text(ufo, x, y,1)
oled.show()

while True:

    #should always at the start and outside if
    oled.fill(0)
    
    if left_button() == 0:
    
        if x <= 0:
            x = 0
        else:
            x_pre = x
            x -= 1
            
        

    if right_button() == 0:
       
        if x == x_edge:
            x = x_edge
            
            oled.text(ufo, x, y,1)
            oled.show()
            
        else:
            x_pres = x
            x += 1
        

    
    if x % 3 == 0: # cannot choose 0 as it will
        oled.text(ufo, x, y,1)
#         if x == 0 and x == x_pre:
#             pass
        oled.show()
        
    

