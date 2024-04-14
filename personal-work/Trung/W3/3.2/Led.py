import time
from machine import UART, Pin, I2C, Timer
from ssd1306 import SSD1306_I2C

I2C_MODE = 1
SCL_PIN = Pin(15)
SDA_PIN = Pin(14)
FREQ = 400000

OLED_WIDTH = 128
OLED_HEIGHT = 64
row_starting = 0
row_edge = OLED_WIDTH - 1

height_starting = 0
height_edge = OLED_HEIGHT -1



i2c = I2C (I2C_MODE, scl = SCL_PIN, sda = SDA_PIN,  freq = FREQ)
oled = SSD1306_I2C(OLED_WIDTH, OLED_HEIGHT, i2c)

letter_height = 8
letter_width = 8
text1 = 'LED1 - OFF'
text2 = 'LED2 - OFF'
text3 = 'LED3 - OFF'
str_len = len(text1) * letter_width
middle_str = int(round((str_len /2),0))
x_middle = int(round(OLED_WIDTH / 2, 0)) #0 - 127
y_bottom = OLED_HEIGHT - letter_height # 0 - 64
x_edge = row_edge - str_len 

x_starting = x_middle - middle_str
y_starting = y_bottom
color = 1
x_pre = 0

oled.fill(0)

oled.text(text1, x_starting, 0 ,1)
# oled.fill_rect(0,letter_height, 128, letter_height, 1)   # draw a solid rectangle 10,10 to 117,53, colour=1

oled.text(text2, x_starting, letter_height ,1)
oled.text(text3, x_starting, 2 * letter_height ,1)
oled.show()