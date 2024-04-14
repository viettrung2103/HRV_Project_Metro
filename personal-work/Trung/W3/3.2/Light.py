from machine import Pin, ADC
import time


on = 1 # for led, 1 is on, 0 is off
off = 0

class Led:
    def __init__(self,pin):
        self.led = Pin(pin, mode = Pin.OUT)
        self.status = 0 # 1 == off
        
    def is_on(self):
        if self.status == on:
            return True
        else:
            return False
        
    def turn_on(self):
        self.led.value(on)
        
    def turn_off(self):
        self.led.value(off)
    
    def run(self):
        if self.is_on():
            self.turn_on()
        else:
            self.turn_off()
        
 
led1 = Led(20)
while True:
        led1.run()
    
