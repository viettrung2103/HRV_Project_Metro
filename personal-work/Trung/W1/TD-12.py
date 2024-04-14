import time
from machine import UART, Pin, I2C, Timer
from ssd1306 import SSD1306_I2C
import framebuf

UP_PIN = 7
DOWN_PIN= 9
RS_PIN = 8

I2C_TYPE = 1
SCL_PIN = Pin(15)
SDA_PIN = Pin(14)
FREQ = 400000

OLED_WIDTH = 128
OLED_HEIGHT = 64

FONT_WIDTH = 8
FONT_HEIGHT = 8


i2c = I2C (I2C_TYPE, scl = SCL_PIN, sda = SDA_PIN,  freq = FREQ)
oled = SSD1306_I2C(OLED_WIDTH, OLED_HEIGHT, i2c)

#buff_frame setting
FRAME_WIDTH        = 84 # width of bufframe
FRAME_HEIGHT       = 64 # height of bufframe
format       = framebuf.MONO_VLSB # vertical bit
bitsPerPixel = 1

# mono so only need 1 bit / pixel >> convert 1 bit to 1/8 byte to find required bytes for this array
fbuf_array =  bytearray(round(FRAME_WIDTH * FRAME_HEIGHT * bitsPerPixel / 8),0) 
fbuf   = framebuf.FrameBuffer(fbuf_array, FRAME_WIDTH, FRAME_HEIGHT, format)

#reset state
fbuf.fill(0)

#starting position
x = 0 #first row
row_8 = 56
y = 0
color = 1
goodbye_text = 'Thank you'


while True:
    text = input("What do you want to type( type quit to quit)? " )
    
    if text == "quit":
        if y > row_8:
            y = row_8
            fbuf.scroll(0, - FONT_HEIGHT)
            fbuf.rect(x,row_8, FRAME_WIDTH, FONT_HEIGHT, False,1)


        fbuf.text(goodbye_text, x, y, color)
        oled.blit(fbuf,0,0)
        oled.show()
        break
    
    if y > row_8: #text is at 9th row
        y = row_8
        fbuf.scroll(0, - FONT_HEIGHT)
        fbuf.rect(x,row_8, FRAME_WIDTH, FONT_HEIGHT, False,1) #True,1 : fill rectangle with color = 1
        
    fbuf.text(text, x, y, color)
    y += FONT_HEIGHT

    
    #paste frame onto screen with blit and show
    oled.blit(fbuf,0,0)
    oled.show()
    
    