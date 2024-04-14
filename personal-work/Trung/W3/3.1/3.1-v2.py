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
        self.a.irq (handler = self.handler, trigger = Pin.IRQ_RISING, hard = True)
        self.press_state = 1
    
    def handler(self,pin):
        #when knob is rotates, check state of b, if b is 1, turn clockwise, if b is 0, turn anti clockwise
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
#                 print("sw is pressed")          
                self.press_state = self.press_state ^ 1
                print("press state = ", self.press_state)
                return 0
            return 1
        return 1
    
    

class Pmw:
    def __init__(self,pin,frequency):
        self.pmw = PWM(pin, frequency)
#         self.rot_sw = rot_sw
        self.duty = 0
        self.adc = 0
        self.saved_adc = 0
        self.rate_of_change = 0
        self.led_state = 1  # 1 is off
        
    def find_rate_of_change(self,encoder):
        if encoder.fifo.has_data():
#             print("fifo has data")

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
#         self.led_state = self.led_state ^ 1
        if self.is_on(): # turn on >> turn off
            self.led_state = 1
        else: #turn off >> turn on
            self.led_state = 0
            
    def save_adc(self):
        self.saved_adc = adc
        self.adc = 0
            
        
            
    def is_on(self):
        if self.led_state == 0:
            return True
        else:
            return False
        
    def check_led_state(self, encoder):
#         print("led state ",self.led_state)
        if encoder.is_pressed():
            
            print("is pressed")
            self.led_state = encoder.pressed()
#         self.led_state
        
    def program(self,encoder):
        
#         if encoder.is_pressed():
#         print("change state")
#         print("led state ", self.led_state)
#             self.led_state = self.turn_state()
        self.led_state = encoder.pressed()
        

        
            
            
        if self.is_on():
#             print("led is on", self.is_on())

#             print("led state ", self.led_state)
            self.fade(encoder)
        else:
            self.pmw.duty_u16(0)
        
    def fade(self, encoder):
#         while True:
        while self.is_on():
#             if encoder.pressed(): 
#                 self.turn_state()
                
#             if self.is_on():
#                 
            if encoder.fifo.empty():
#                 print("fifo is empty")
#                 print("adc ", adc)
                self.pmw.duty_u16(self.adc)
            else:
#                 print("led is on ", self.is_on())
#                 while encoder.fifo.has_data():
                rate_of_change = self.find_rate_of_change(encoder)
#                 print("rate of change ",rate_of_change)
                self.duty = self.find_duty(rate_of_change)
#                 print("duty ",self.duty)
                adc_value = self.duty * adc / hundred_percent
                self.adc = int(round(adc_value,0))
#                 print("adc value ",self.adc)
                self.pmw.duty_u16(self.adc)
#                 sleep(0.1)
            self.check_led_state(encoder)
#                 print("duty_cycle",duty_cycle)
        
#         print("duty",duty)

#                 duty = duty + rate_of_change
                
        
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
            
rot = Encoder(10,11,12)

frequency = 1000
pin = Pin(20)

pwm = Pmw(pin,frequency)

while True:
#     press = rot.pressed()
#     if press:
# 
#         print(press)
#     pwm.fade(rot)
    pwm.program(rot)

        
            
