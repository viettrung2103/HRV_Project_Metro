import time
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C

sw0 = Pin(9, Pin.IN, Pin.PULL_UP)
sw2 = Pin(8, Pin.IN, Pin.PULL_UP)
i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
oled_width = 128
oled_height = 64
oled = SSD1306_I2C(oled_width, oled_height, i2c)


UFO = "<=>"
move = 0

while True:
    if sw0.value() == 0:  
        move += 1 
        if move >= oled_width - len(UFO)*8:  
            move = oled_width - len(UFO)*8
    
    if sw2.value() == 0:  
        move -= 1  
        if move < 0:  
            move = 0
    
    oled.fill(0)  
    oled.text(UFO, move, 50, 1)  
    oled.show() 
    
    time.sleep(0.001)
