from machine import Pin, PWM
from fifo import Fifo
import micropython
import time
micropython.alloc_emergency_exception_buf(200)


light_mode = 0


class Encoder:
    def __init__(self, rot_a, rot_b):
        self.a = Pin(rot_a, mode=Pin.IN, pull=Pin.PULL_UP)
        self.b = Pin(rot_b, mode=Pin.IN, pull=Pin.PULL_UP)
        self.fifo = Fifo(30, typecode="i")
        self.a.irq(handler=self.handler, trigger=Pin.IRQ_RISING, hard=True)
    
    def handler(self, pin):
        if light_mode != 0:
            if self.b():
                self.fifo.put(-1)
            else:
                self.fifo.put(1)

class Led:
    def __init__(self, pin):
        self.pwm = PWM(Pin(pin))

    def turn_on(self, brightness):
        self.pwm.freq(1000)  
        self.pwm.duty_u16(int(brightness * 655.35)) 
        
class Program:
    def __init__(self,encoder, led):
        self.encoder = encoder
        self.led = led
        self.bright = 0
        
    def read_fifo(self):
        while self.encoder.fifo.has_data():
            dosang = rot.fifo.get()
            if dosang == 1:
                self.bright += 5
                if self.bright >= 100:
                    self.bright = 100
#                 print("brightness:",self.bright)
                    
            elif dosang == -1:
                self.bright -= 5
                if self.bright < 0:
                    self.bright = 0 
#                 print("brightness:",self.bright)
        
class Nut12:
    mode = None
    def __init__(self,pin):
        self.pin = Pin(pin, Pin.IN, Pin.PULL_UP)
        
    def press(self):
        if self.pin.value() == 0:
            mode = 1
        elif self.pin.value() ==1:
            mode = 0
        

rot = Encoder(10, 11)
led1 = Led(20)
x=Program(rot,led1)
pressbutton = Nut12(12)
No_light = 0

while True:
#         so = x.read_fifo()
#     x.led.turn_on(x.bright)
    if pressbutton.pin.value() == 0: # DEN TAT
        while pressbutton.pin.value() == 0:
            pass
        time.sleep(0.05)
        light_mode ^= 1
#         print("tinh trang",press12)
    if light_mode == 0:

        x.led.turn_on(0)
#         print("den khong sang nua",press12)
#         pass
    else:
#         print("den sang",press12)
        so = x.read_fifo()
        x.led.turn_on(x.bright)
           

    

    
    
