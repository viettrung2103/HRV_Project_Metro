from machine import Pin, ADC, PWM
import time

# rot_push = Pin(12, mode = Pin.IN, pull = Pin.PULL_UP)
sw = Pin(12, pull = Pin.PULL_UP, mode = Pin.IN)
a = 1

def sw_is_pressed():
    if sw.value() == 0:
        return True
    else:
        return False


# while True:
#     #when is pressed and released, print 
#     if sw.value() == 0:
#         while sw.value() == 0:
#             pass
#         time.sleep(0.1)
#         print("button pressed")
#         a = a ^ 1
#         print("a = ", a )
        
#         
#         if sw.value() == 0:
#             print("button pressed")

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
            time.sleep(0.05)
            # the while only work if sw is not an object
#             while self.is_pressed() == 0:
            if self.is_pressed() == 0:
                
                   
                self.a = self.a ^ 1
                print("a = ", self.a)
                return True
        
        return False
#         if self.is_pressed():
#             time.sleep(0.050)
#             if self.is_pressed() == 0:
#                 return True
#             
#         return False

rot_sw = Rot_SW(12)

while True:
    if rot_sw.pressed():
        print("sw is pressed")
        print(rot_sw.pressed())

    
    