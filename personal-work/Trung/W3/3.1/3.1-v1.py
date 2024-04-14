
from machine import Pin, PWM
from fifo import Fifo
from time import sleep

import micropython
micropython.alloc_emergency_exception_buf(200)

class Encoder:
    def __init__ (self, rot_a, rot_b,fifo, pmw):
        self.a = Pin(rot_a, mode = Pin.IN, pull = Pin.PULL_UP)
        self.b = Pin(rot_b, mode = Pin.IN, pull = Pin.PULL_UP)
#         self.fifo = Fifo(30, typecode = "i")
        self.fifo = fifo
        self.a.irq (handler = self.handler, trigger = Pin.IRQ_RISING, hard = True)
        self.pmw = pmw
    
    def handler(self,pin):
        #when knob is rotates, check state of b, if b is 1, turn clockwise, if b is 0, turn anti clockwise
        if pmw.is_led():
            print("led is on ",pmw.is_led())
            if self.b():
                self.fifo.put(-1)
            else:
                self.fifo.put(1)
                



class Rot_SW :
    def __init__(self, pin):
        self.rot_sw = Pin(pin, pull = Pin.PULL_UP, mode = Pin.IN)
        self.a = 1
    
    def is_pressed(self):
        if self.rot_sw.value() == 0:
            return True
        else:
            return False
        
    def pressed(self):
        if self.is_pressed():
            sleep(0.05)
            # the while only work if sw is not an object
#             while self.is_pressed() == 0:
            if self.is_pressed() == 0:
                
                   
                self.a = self.a ^ 1
#                 print("a = ", self.a)
                return True
        
        return False

# frequency = 1000
# pin = Pin(20)
# 
# pwd = PWM(pin,frequency)
# # led = Pin(pwd,Pin.OUT)
# # led.off()
# adc = 2 ** 16
# while True:
#     for duty_cycle in range(0,100):
#         adc_value = duty_cycle * adc / 100
#         duty_value = int(round(adc_value,0))
#         
#             
#         print("duty_cycle",duty_cycle)
#         
# #         print("duty",duty)
#         pwd.duty_u16(duty_value)
#         sleep(0.05)

adc = 2 ** 16

class Pmw:
    def __init__(self,pin,frequency, rot_sw):
        self.pmw = PWM(pin, frequency)
        self.rot_sw = rot_sw
    
    #0-100
    def fade(self,duty_cycle, fifo):
#         print("pmw is led", self.is_led())
        print(duty_cycle)
        if self.is_led():
            if fifo.empty():
                self.pmw.duty_u16(duty_value)
            else:
                while fifo.has_data():
                    
                    
    #             while fifo.has_data():
    #             print("fifo",fifo.get())

    #                 print("duty value ",duty_value)
                    
                    data = fifo.get() * 10
                    adc_value = duty_cycle * adc / 100
                    if adc_value == 100:
                        adc_value = 100
                    else:
                        adc_value = adc_value + data
        #                 print("adc value ",adc_value)
                    duty_value = int(round(adc_value,0))
                    self.pmw.duty_u16(duty_value)
#         sleep(0.05)
        else:
#             print("led is on", self.is_led())
            self.pmw.duty_u16(0)

    def is_led(self):
        if self.rot_sw.a == 1:
            return True
        else:
            return False
        
        
class Led:
    def __init__(self,pin):
        self.led = Pin(pin, mode = Pin.OUT)
        
    def turn_on(self,rot_sw):
        if rot_sw.a == 0:
            self.led.off()
        if rot_sw.a == 1:
            self.led.on()
            
            
fifo = Fifo(30, typecode = "i")           
rot_sw = Rot_SW(12)
led = Led(20)
pmw = Pmw(20,1000, rot_sw)
rot = Encoder(10,11,fifo,pmw)


while True:
    if rot_sw.pressed():
#         print("pmw is led ", pmw.is_led())
#         if pmw.is_led():
#         print("sw is pressed")
#         led.turn_on(rot_sw)
        pmw.fade(100,fifo)


