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


while True:
    #when is pressed and released, print 
    if sw.value() == 0:
        while sw.value() == 0:
            pass
        time.sleep(0.1)
        print("button pressed")
#         a = a ^ 1
#         print("a = ", a )
        
#         
#         if sw.value() == 0:
#             print("button pressed")
    
    