import time
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C

i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
oled_width = 128
oled_height = 64
oled = SSD1306_I2C(oled_width, oled_height, i2c)

max_lines = oled_height // 8
line_list = []

def scroll_display(): #call dx and dy. we remain dx and scroll up dy by -8 pixel
    oled.scroll(0, -8)

def draw_text(lines):
    oled.fill(0)
    for i, line in enumerate(lines):
        oled.text(line, 0, i * 8)
    oled.show()

while True:
    user_input = input("Enter text (press Enter to submit):\n")
    line_list.append(user_input)
    if len(line_list) > max_lines:
        line_list.pop(0)
    draw_text(line_list)
