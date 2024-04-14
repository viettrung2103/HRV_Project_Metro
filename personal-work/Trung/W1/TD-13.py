import time
from machine import UART, Pin, I2C, Timer
from ssd1306 import SSD1306_I2C

UP_PIN = 7
DOWN_PIN= 9
RS_PIN = 8

I2C_TYPE = 1
SCL_PIN = Pin(15)
SDA_PIN = Pin(14)
FREQ = 400000

OLED_WIDTH = 128
OLED_HEIGHT = 64



up_btn = Pin(UP_PIN, Pin.IN, Pin.PULL_UP)
down_btn = Pin(DOWN_PIN, Pin.IN, Pin.PULL_UP)
rs_btn = Pin(RS_PIN, Pin.IN, Pin.PULL_UP)

i2c = I2C (I2C_TYPE, scl = SCL_PIN, sda = SDA_PIN,  freq = FREQ)
oled = SSD1306_I2C(OLED_WIDTH, OLED_HEIGHT, i2c)

letter_height = 8
letter_width = 8
row_starting = 0
row_edge = OLED_WIDTH - 1

height_starting = 0
height_edge = OLED_HEIGHT -1




#starting position


x_middle = int(round(OLED_WIDTH / 2, 0)) #0 - 127
y_middle = int(round(OLED_HEIGHT / 2, 0)) #0 - 127




x = 0
y = y_middle
color = 1
x_pre = 0

def reset():
    oled.fill(0)
    x = 0
    y = y_middle
    
    return x, y

oled.fill(0)
while True:

    oled.pixel( x, y, color)
    
    if x == row_edge:
        x = 0
    x += 1

    if up_btn() == 0:
    
        if y == 0:
            y = 0
        else:
            y_pre = y
            y -= 1
    
    if down_btn() == 0:
        
        if y == height_edge:
            y = height_edge
        else:
            y_pre = y
            y += 1
            
    if rs_btn() == 0:
        x,y  = reset()

    
    if x % 1 == 0: # cannot choose 0 as it will
        oled.pixel( x, y, color)
    #         if x == 0 and x == x_pre:
#             pass
        oled.show()
#     oled.show()


