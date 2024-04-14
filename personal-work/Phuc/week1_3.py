import time
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C

sw0 = Pin(8, Pin.IN, Pin.PULL_UP)
sw1 = Pin(7, Pin.IN, Pin.PULL_UP)
sw2 = Pin(9, Pin.IN, Pin.PULL_UP)

i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
oled_width = 128
oled_height = 64
oled = SSD1306_I2C(oled_width, oled_height, i2c)

up_down = 0
line = oled_height // 2
move = 1  

def clear_screen():
    oled.fill(0)
    oled.show()

def draw_line(x, y):
    oled.pixel(x, y, 1)
    oled.show()


while True:
    if sw1.value() == 0:
        clear_screen()
        up_down = 0
        line = oled_height // 2
        move = 1

    up_down += move

    if up_down >= oled_width:
        up_down = 0

    if sw0.value() == 0:
        line -= 1
        if line < 1:
            line = 0
    elif sw2.value() == 0:
        line += 1
        if line >= oled_height:
            line = oled_height - 1

    draw_line(up_down, line)

    time.sleep(0.005)
