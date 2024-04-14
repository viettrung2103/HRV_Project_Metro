from machine import Pin, ADC, PWM
from time import sleep

#frequency should be 1000~ 
frequency = 1000
pin = Pin(20)

pwd = PWM(pin,frequency)
# led = Pin(pwd,Pin.OUT)
# led.off()
adc = 2 ** 16-1
while True:
    for duty_cycle in range(0,100):
#         duty_cycle = 10
        adc_value = duty_cycle * adc / 100
        duty_value = int(round(adc_value,0))

            
        print("duty_cycle",duty_cycle)
        print("duty_value",duty_value)


        #         print("duty",duty)
        pwd.duty_u16(duty_value)
        sleep(0.05)
#         led.on()
# pwd.duty_u16(8000)                       