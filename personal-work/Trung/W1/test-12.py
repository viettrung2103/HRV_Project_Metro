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



up_btn = Pin(UP_PIN, Pin.IN, Pin.PULL_UP)
down_btn = Pin(DOWN_PIN, Pin.IN, Pin.PULL_UP)
rs_btn = Pin(RS_PIN, Pin.IN, Pin.PULL_UP)

i2c = I2C (I2C_TYPE, scl = SCL_PIN, sda = SDA_PIN,  freq = FREQ)
oled = SSD1306_I2C(OLED_WIDTH, OLED_HEIGHT, i2c)

FRAME_WIDTH        = 84
FRAME_HEIGHT       = 72
format       = framebuf.MONO_VLSB
bitsPerPixel = 1

# mono so only need 1 bit / pixel >> convert 1 bit to 1/8 byte to find required bytes for this array
fbuf_array =  bytearray(round(FRAME_WIDTH * FRAME_HEIGHT  * bitsPerPixel / 8),0) 
fbuf   = framebuf.FrameBuffer(fbuf_array, FRAME_WIDTH, FRAME_HEIGHT , format)

                         
fbuf.fill(0)
fbuf.text('hi',0,0,1)
fbuf.text('ba',0,8,1)
fbuf.text('bon',0,16,1)
fbuf.text('nam',0,24,1)
fbuf.text('sau',0,32,1)
fbuf.text('bay',0,40,1)
fbuf.text('tam',0,48,1)
fbuf.text('9',0,56,1)
fbuf.text('10',0,64,1)

#always, rows at the edge will be duplicate

fbuf.scroll(0,-8)
fbuf.rect(0,56, FRAME_WIDTH, 8, False,1)
fbuf.text('11',0,56,1)
# fbuf.scroll(0,-8)



oled.blit(fbuf,0,0)
oled.show()