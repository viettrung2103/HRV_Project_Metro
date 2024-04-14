from machine import Pin, PWM
from fifo import Fifo
from time import sleep
import micropython
micropython.alloc_emergency_exception_buf(200)


adc = 2 ** 16 -1
rate_step =5
max_duty = 100
min_duty = 0
hundred_percent = 100


class Encoder:
    def __init__ (self, rot_a, rot_b, rot_pin):
        self.a = Pin(rot_a, mode = Pin.IN, pull = Pin.PULL_UP)
        self.b = Pin(rot_b, mode = Pin.IN, pull = Pin.PULL_UP)
        self.rot_sw = Pin(rot_pin, pull = Pin.PULL_UP, mode = Pin.IN)

        self.fifo = Fifo(30, typecode = "i")
        self.a.irq (handler = self.handler, trigger = Pin.IRQ_FALLING, hard = True)
        self.press_state = 1
        #change to irq-fall, change b, or change in handler to change rot directino
    
    def handler(self,pin):
        #when knob is rotates, check state of b, if b is 1, turn clockwise, if b is 0, turn anti clockwise
        if self.press_state == 0: # is press to turn on light
            if self.b():
                self.fifo.put(1)
            else:
                self.fifo.put(-1)
            
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
     
                self.press_state = self.press_state ^ 1
#                 print("press state = ", self.press_state)

        return self.press_state
    
    

class Pmw:
    def __init__(self,pin,frequency):
        self.pmw = PWM(pin, frequency)
        self.duty = 0
        self.adc = 0
        self.saved_adc = 0
        self.rate_of_change = 0
        self.led_state = 1  # 1 is off
        
    def find_rate_of_change(self,encoder):
        if encoder.fifo.has_data():
            self.rate_of_change = encoder.fifo.get() * rate_step
        else:
            self.rate_of_change = 0
        return self.rate_of_change 
             
    def find_duty(self, rate_of_change):
        self.duty = self.duty + rate_of_change
        if self.duty >= max_duty:
            self.duty = max_duty
        if self.duty <= min_duty:
            self.duty = min_duty
        return self.duty
    
    def turn_state(self):
        if self.is_on(): # turn on >> turn off
            self.led_state = 1
        else: #turn off >> turn on
            self.led_state = 0
            
    def is_on(self):
        if self.led_state == 0:
            return True
        else:
            return False
        
    def check_led_state(self, encoder):
        if encoder.is_pressed():
            self.led_state = encoder.pressed()

        
    def program(self,encoder):
        self.led_state = encoder.pressed()
        if self.is_on():
            self.fade(encoder)
        else:
            self.pmw.duty_u16(0)
            
    def find_adc(self,encoder):
        rate_of_change = self.find_rate_of_change(encoder)
        self.duty = self.find_duty(rate_of_change)
        adc_value = self.duty * adc / hundred_percent
        return int(round(adc_value,0))
        
    def fade(self, encoder):
        while self.is_on():
            if encoder.fifo.empty():
                self.pmw.duty_u16(self.adc)
            else:
                self.adc = self.find_adc(encoder)
                self.pmw.duty_u16(self.adc)
            self.check_led_state(encoder)

               
rot = Encoder(10,11,12)

frequency = 1000
pin = Pin(20)

pwm = Pmw(pin,frequency)

while True:

    pwm.program(rot)

        
            

