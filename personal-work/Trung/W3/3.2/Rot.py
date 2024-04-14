from machine import Pin
from fifo import Fifo
import micropython
micropython.alloc_emergency_exception_buf(200)

class Encoder:
    def __init__ (self, rot_a, rot_b):
        self.a = Pin(rot_a, mode = Pin.IN, pull = Pin.PULL_UP)
        self.b = Pin(rot_b, mode = Pin.IN, pull = Pin.PULL_UP)
        self.turn_fifo = Fifo(30, typecode = "i")
        self.a.irq (handler = self.handler, trigger = Pin.IRQ_RISING, hard = True)
    
    def handler(self,pin):
        #when knob is rotates, check state of b, if b is 1, turn clockwise, if b is 0, turn anti clockwise
        if self.b():
            self.turn_fifo.put(1)
        else:
            self.turn_fifo.put(-1)
            

            
rot = Encoder(10,11)

while True:
    while rot.turn_fifo.has_data():
        print(rot.turn_fifo.get())
            
