import time
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import micropython
micropython.alloc_emergency_exception_buf(200)
i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)

class OLED_Menu:
    def __init__(self, width, height):
        self.oled = SSD1306_I2C(width, height, i2c)
        self.width = width
        self.height = height
        self.menu_items = ["LED1 - OFF", "LED2 - OFF", "LED3 - OFF"]
        self.count = 0
        self.update()

    def update(self):
        self.oled.fill(0)
        for i, item in enumerate(self.menu_items):
            self.oled.text(item, 24, i * 10)
        self.oled.text("[", 12, self.count * 10)
        self.oled.text("]",108, self.count * 10)
        self.oled.show()

    def move_down(self):
        self.count +=1
        if self.count > 2:
            self.count = 0
        self.update()

    def move_up(self):
        self.count -=1
        if self.count< 0:
            self.count = 2
        self.update()

    def toggle_state(self):
        item = self.menu_items[self.count]
        if "ON" in item:
            self.menu_items[self.count] = item.replace("ON", "OFF")
            if self.count== 0:
                led1.off()
            elif self.count == 1:
                led2.off()
            elif self.count == 2:
                led3.off()
        else:
            self.menu_items[self.count] = item.replace("OFF", "ON")
            if self.count == 0:
                led1.on()
            elif self.count == 1:
                led2.on()
            elif self.count == 2:
                led3.on()
        self.update()


oled = OLED_Menu(128, 64)


led1 = Pin(22, Pin.OUT)
led2 = Pin(21, Pin.OUT)
led3 = Pin(20, Pin.OUT)

button_down = Pin(10, Pin.IN, Pin.PULL_UP)
button_up = Pin(11, Pin.IN, Pin.PULL_UP)
button_select = Pin(12, Pin.IN, Pin.PULL_UP)

button_down_state = 1
button_up_state = 1
button_select_state = 1
while True:
    if button_down.value() == 0 and button_down_state == 1:
        while button_down.value() == 0 and button_down_state == 1:
            pass
        button_down_state ^=1
        oled.move_down()
        time.sleep(0.05) 
    else:
        button_down_state = 1

    if button_up.value() == 0 and button_up_state == 1:
        while button_up.value() == 0 and button_up_state == 1:
            pass
        button_up_state ^=1
        oled.move_up()
        time.sleep(0.05)
    else:
        button_up_state = 1

    if button_select.value() == 0 and button_select_state == 1:

        while button_select.value() == 0 and button_select_state == 1:
            pass
        button_select_state ^=1
        oled.toggle_state()
        time.sleep(0.05)
    else:
        button_select_state = 1
