from machine import Pin
from fifo import Fifo
import micropython
micropython.alloc_emergency_exception_buf(200)

class Encoder:
    def __init__ (self, rot_a, rot_b):
        self.a = Pin(rot_a, mode = Pin.IN, pull = Pin.PULL_UP)
        self.b = Pin(rot_b, mode = Pin.IN, pull = Pin.PULL_UP)
        self.fifo = Fifo(30, typecode = "i")
        self.a.irq (handler = self.handler, trigger = Pin.IRQ_RISING, hard = True)
    
    def handler(self,pin):
        #when knob is rotates, check state of b, if b is 1, turn clockwise, if b is 0, turn anti clockwise
        if self.b():
            self.fifo.put(1)
        else:
            self.fifo.put(-1)
            
# class Led:
#     def __init__(self,pin):
#         self.led = Pin(pin, mode = Pin.OUT)
#         
# #     def turn_on(self,rot_sw):
# #         if rot_sw.a == 0:
# #             self.led.off()
# #         if rot_sw.a == 1:
# #             self.led.on()
#             
#     def turn_on(self, degre):
#         bright = 
            
rot = Encoder(10,11)

while True:
    while rot.fifo.has_data():
        print(rot.fifo.get())
            