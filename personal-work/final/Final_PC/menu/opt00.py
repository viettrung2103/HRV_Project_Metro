# from machine import UART, Pin, I2C, Timer
from ssd1306 import SSD1306_I2C
from fifo import Fifo


from machine import UART, Pin, I2C, Timer, ADC
from piotimer import Piotimer
import math
import time

from encoder import Isr_Fifo, Encoder
from opt10 import Opt10, Opt10_Display

import micropython
micropython.alloc_emergency_exception_buf(200)




# const for display
I2C_MODE = 1
SCL_PIN = Pin(15)
SDA_PIN = Pin(14)
FREQ = 400000

OLED_WIDTH = 128
OLED_HEIGHT = 64
ROW_START = 0
ROW_EDGE = OLED_WIDTH - 1 #127
HEIGHT_START = 0
HEIGHT_EDGE = OLED_HEIGHT -1 #63

BLANK = 0
FILLED = 1
COLUMN_SPACE = 2
LETTER_HEIGHT = 8
LETTER_WIDTH = 8
Y_ROW_1 = 0
Y_ROW_2 = COLUMN_SPACE + LETTER_HEIGHT
Y_ROW_3 = Y_ROW_2 + COLUMN_SPACE + LETTER_HEIGHT
Y_ROW_4 = Y_ROW_3 + COLUMN_SPACE + LETTER_HEIGHT

#const for led
LED1_PIN = Pin(22)
LED2_PIN = Pin(21)
LED3_PIN = Pin(20)
ON = 1 # for led, 1 is on, 0 is off
OFF = 0



#hr
t = 4 #4ms
frequency = 250
MINUTE = 60
SECOND = 1
THOUSAND = 1000
TWO = 2
test_duration = TWO  * SECOND * THOUSAND # to ms
duration = TWO * SECOND * THOUSAND

# total_time = 2 * SECOND
test_sample_size =round(test_duration / t , 0)
sample_size = round(duration / t, 0)
step = 3

age = 30
# MIN_HR = 50
# MAX_HR = 240 - age
MIN_HR = 50
MAX_HR = 150

# MIN_PULSE = 1
# MAX_PULSE = 6

MAX_ADC = 2 ** 16 -1
MIN_ADC = 0
DELTA = MAX_ADC - MIN_ADC
PERCENT = 0.12
LOWER_LIM = round(DELTA * PERCENT,0)

#for encoder
ROT_A_PIN = Pin(10)
ROT_B_PIN = Pin(11)
ROT_SW_PIN = Pin(12)
BOUNCE_TIME = 200

Y_ROW_1 = 0
Y_ROW_2 = COLUMN_SPACE + LETTER_HEIGHT
Y_ROW_3 = Y_ROW_2 + COLUMN_SPACE + LETTER_HEIGHT
Y_ROW_4 = Y_ROW_3 + COLUMN_SPACE + LETTER_HEIGHT
Y_ROW_5 = Y_ROW_4 + COLUMN_SPACE + LETTER_HEIGHT


# 
#  
# class Isr_Fifo(Fifo):
#     def __init__(self, size, adc_pin_nr):
#         super().__init__(size)
#         self.av = ADC(adc_pin_nr)
#         self.dbg = Pin(0,Pin.OUT)
#         self.cur_program = None
#         self.stop_flag = False
#         # self.display = display
#         
#     def update_program(self,program):
#             self.cur_program = program    
#     
#     def handler_11_or_21(self):
#         if self.stop_flag == False :
#             self.put(self.av.read_u16())
#             self.dbg.toggle()  
#   
#     def handler(self,tid):
#         if self.cur_program != None:
#             name = self.cur_program.name
#             if name == 11 or name == 21 :           
#                 self.handler_11_or_21()
                
# class Isr_Fifo(Fifo):
#     def __init__(self, size, adc_pin_nr):
#         super().__init__(size)
#         self.av = ADC(adc_pin_nr)
#         self.dbg = Pin(0,Pin.OUT)
#         self.cur_program = None
#         self.stop_flag = False
#         # self.display = display
#         
#     def update_program(self,program):
#             self.cur_program = program    
#     
#     def handler_11_or_21(self):
#         if self.stop_flag == False :
#             self.put(self.av.read_u16())
#             self.dbg.toggle()  
#   
#     def handler(self,tid):
#         if self.cur_program != None:
#             name = self.cur_program.name
#             if name == "11" or name == "21" :           
#                 self.handler_11_or_21()
        
# 
# class Encoder:
#     def __init__ (self, rot_a_pin, rot_b_pin, rot_sw_pin):
#         self.a = Pin(rot_a_pin, mode = Pin.IN, pull = Pin.PULL_UP)
#         self.b = Pin(rot_b_pin, mode = Pin.IN, pull = Pin.PULL_UP)
#         self.sw = Pin(rot_sw_pin, pull = Pin.PULL_UP, mode = Pin.IN)
#         self.prev_time = 0
#         
#         self.cur_selector = None
#         self.cur_program  = None
#         # self.press = False
#         self.p00_fifo = Fifo(30)
#         self.t00_fifo = Fifo(30, typecode = "i") #signed = "i"
#         
#         self.p10_fifo = Fifo(30) #default is unsigned "H"
# #         self.t10_fifo = Fifo(30, typecode = "i") #signed = "i"
# 
#         self.p11_fifo = Fifo(30)
#         
#         self.sw.irq(handler = self.press_handler, trigger = Pin.IRQ_RISING, hard = True)
#         self.a.irq (handler = self.turn_handler, trigger = Pin.IRQ_RISING, hard = True)
# 
#     
#     # def update_selector(self,selector):
#     #     self.cur_selector = selector
#         
#     def update_program(self, program):
#         self.cur_program = program
#         self.cur_selector = program.selector
#         
#     def get_press_fifo_number(self):
#         name = self.cur_program.name
#         if name == "00":
#             return self.p00_fifo
#         elif name == "10":
#             
#             return self.p10_fifo
#         elif name == "11":
#             return self.p11_fifo
#         
#     def get_turn_fifo_number(self):
#         name = self.cur_program.name
#         if name == "00":
#             return self.t00_fifo   
# #         elif name == 10:
# #             return self.t10_fifo
#             
#     def press_handler(self,pin):
#         if self.cur_program != None:
#             p_fifo = self.get_press_fifo_number()
#             name = self.cur_program.name
#             cur_time = time.ticks_ms()
#             delta = time.ticks_diff(cur_time, self.prev_time)
#             if delta >= BOUNCE_TIME:
#                 if name == "00":
# #                     print("index ",self.cur_selector.current_pos)
#                     p_fifo.put(self.cur_selector.current_pos)
#                 elif name == "40":
#                     pass
#                 else:
# #                     print("here")
#                     p_fifo.put(1)
#                 self.prev_time = cur_time
#                 
#     def turn_handler(self,pin):
#         if self.cur_selector != None:
#             t_fifo = self.get_turn_fifo_number()
#             if self.b():
#                 t_fifo.put(1)
#             else:
#                 t_fifo.put(-1)  

#             
#             
# class Opt10_Display:
#     def __init__(self, i2c, scl_pin, sda_pin, frequency, oled_w, oled_h):
#         self.i2c = I2C(i2c, scl=scl_pin, sda=sda_pin, freq=frequency)
# #         self.display = SSD1306_I2C(oled_w, oled_h, self.i2c)
#         self.display = SSD1306_I2C(oled_w, oled_h, self.i2c)
#         self.stop_flag = False
#         
#     def reset(self):
#         self.display.fill(0)
#     
#     def show(self):
#         self.reset()
#         self.display.text("Option 10",0,0)
#         self.display.show()
#         
# 
# # class Opt10_Encoder:
# #     def __init__ (self, rot_sw_pin):
# # 
# #         self.sw = Pin(rot_sw_pin, pull = Pin.PULL_UP, mode = Pin.IN)
# #         self.press_state = 1
# #         self.stop_flag = False
# #         self.press = False
# #         self.prev_time = 0
# #         self.press_fifo = Fifo(30) #default is signed "H"
# #         self.sw.irq(handler = self.press_handler, trigger = Pin.IRQ_RISING, hard = True)
# #     
# # 
# #             
# #     def press_handler(self,pin):
# # 
# #         if self.stop_flag == False:
# # #             print("here")
# #             cur_time = time.ticks_ms()
# #         #         print("now ",now)
# #         #         print("then ",then)
# #             delta = time.ticks_diff(cur_time, self.prev_time)
# #         #         print(delta)
# #             if delta >= BOUNCE_TIME:
# #                 self.press_fifo.put(1)
# #                 self.prev_time = cur_time
# 
# def get_x_starting(text):
#     str_len = len(text) * LETTER_WIDTH
#     middle_str = int(round((str_len /2),0))
#     x_middle = int(round(OLED_WIDTH / 2, 0)) #0 - 127
#     x_starting = x_middle - middle_str
#     return x_starting
#         
# class Opt10_selector:
#     def __init__(self,size):
#         self.size =size
# 
# # class Opt10_Display:
# #     def __init__(self, i2c, scl_pin, sda_pin, frequency, oled_w, oled_h):
# #         self.i2c = I2C(i2c, scl=scl_pin, sda=sda_pin, freq=frequency)
# #         self.display = SSD1306_I2C(oled_w, oled_h, self.i2c)
# # #         self.current_flag = True
# #         
# #     def reset(self):
# #         self.display.fill(0)
# #     
# #     def show(self):
# #         text1 = "START "
# #         text2 = "MEASUREMENT"
# #         text3 = "BY"
# #         text4 = "PRESSING"
# #         text5 = "THE BUTTON"
# #         x1 = get_x_starting(text1)
# #         x2 = get_x_starting(text2)
# #         x3 = get_x_starting(text3)
# #         x4 = get_x_starting(text4)
# #         x5 = get_x_starting(text5)
# #         self.reset()
# #         self.display.text(text1,x1,Y_ROW_1)
# #         self.display.text(text2,x2,Y_ROW_2)
# #         self.display.text(text3,x3,Y_ROW_3)
# #         self.display.text(text4,x4,Y_ROW_4)
# #         self.display.text(text5,x5,Y_ROW_5)
# #         self.display.show()
# 
# class Opt10:
#     def __init__(self,name,display, encoder,isr_fifo, selector = None):
# #         self.opt10_display = opt10_display
#         self.name = name
#         self.display = display
#         self.encoder = encoder
#         self.isr_fifo = isr_fifo
#         self.stop_flag = False
# #         self.press_flag = False
#         self.selector = selector
#         self.press = False
#         
#     def is_active(self):
#         return self.current_flag
# 
#     
#     def on(self):
#         self.press = False
#         self.current_flag = True
#         self.encoder.update_program(self)
# #         self.encoder.update_selector(self.selector)
# #         self.display.show()
# #         self.handle_press()
#         self.run()
# #         self.handle_turn()
# 
#     def run(self):
#         self.display.show()
#         self.handle_press()
# #         
#         
#     def handle_press(self):
#         p10_fifo = self.encoder.p10_fifo
#         # print(self.encoder.cur_program.name)
#         while p10_fifo.has_data():
#             value = p10_fifo.get()
#             print(f"program {self.name} value {value}")
#             if value == 1:
# 
#                 self.press = True
#             
# #     def handle_turn(self):
# #         t10_fifo = self.encoder.t10_fifo
# #         while t10_fifo.has_data():
# #             value = t10_fifo.get()
# #             self.selector.size += value
# #             print(f"program: {self.name} selector: {self.selector.size}")
#         
# 
#     def off(self):
#         self.current_flag = False
# 
#         self.encoder.current_flag = False

# 
# def get_x_starting(text):
#     str_len = len(text) * LETTER_WIDTH
#     middle_str = int(round((str_len /2),0))
#     x_middle = int(round(OLED_WIDTH / 2, 0)) #0 - 127
#     x_starting = x_middle - middle_str
#     return x_starting
#         
# class Opt10_selector:
#     def __init__(self,size):
#         self.size =size
# 
# class Opt10_Display:
#     def __init__(self, i2c, scl_pin, sda_pin, frequency, oled_w, oled_h):
#         self.i2c = I2C(i2c, scl=scl_pin, sda=sda_pin, freq=frequency)
#         self.display = SSD1306_I2C(oled_w, oled_h, self.i2c)
# #         self.current_flag = True
#         
#     def reset(self):
#         self.display.fill(0)
#     
#     def show(self):
#         text1 = "START "
#         text2 = "MEASUREMENT"
#         text3 = "BY"
#         text4 = "PRESSING"
#         text5 = "THE BUTTON"
#         x1 = get_x_starting(text1)
#         x2 = get_x_starting(text2)
#         x3 = get_x_starting(text3)
#         x4 = get_x_starting(text4)
#         x5 = get_x_starting(text5)
#         self.reset()
#         self.display.text(text1,x1,Y_ROW_1)
#         self.display.text(text2,x2,Y_ROW_2)
#         self.display.text(text3,x3,Y_ROW_3)
#         self.display.text(text4,x4,Y_ROW_4)
#         self.display.text(text5,x5,Y_ROW_5)
#         self.display.show()
# 
# class Opt10:
#     def __init__(self,name,encoder, display, selector = None):
# #         self.opt10_display = opt10_display
#         self.name = name
#         self.display = display
#         self.encoder = encoder
#         self.current_flag = True
# #         self.press_flag = False
#         self.selector = selector
#         self.press = False
#         
#     def is_active(self):
#         return self.current_flag
# 
#     
#     def on(self):
#         self.press = False
#         self.current_flag = True
#         self.encoder.update_program(self)
# #         self.encoder.update_selector(self.selector)
#         self.display.show()
#         self.handle_press()
# #         self.handle_turn()
# 
#         
#     def handle_press(self):
#         p10_fifo = self.encoder.p10_fifo
#         while p10_fifo.has_data():
#             value = p10_fifo.get()
#             if value == 1:
#                 
#                 self.press = True
#             
# #     def handle_turn(self):
# #         t10_fifo = self.encoder.t10_fifo
# #         while t10_fifo.has_data():
# #             value = t10_fifo.get()
# #             self.selector.size += value
# #             print(f"program: {self.name} selector: {self.selector.size}")
#         
# 
#     def off(self):
#         self.current_flag = False
# 
#         self.encoder.current_flag = False

        
class Program:
  def __init__(self,name):
    self.name = name
    
  def run(self):
    print(self.name)

class Opt00_Display:
    def __init__(self,i2c,scl_pin,sda_pin,frequency,oled_w, oled_h):
        self.i2c = I2C(i2c, scl=scl_pin, sda = sda_pin, freq = frequency)
        self.display = SSD1306_I2C(oled_w, oled_h, self.i2c)
        self.program_str_list = []       
        
    def add_text(self,text):
        self.program_str_list.append(text)
        
    def reset(self):
        self.display.fill(0)
        

    def show_result(self,selector):
        self.reset()
        for index, program_str in enumerate(self.program_str_list):
            if selector.current_pos == index:
                self.display.text(selector.str, selector.x_loc, selector.y_loc, 1)
            else:
                self.display.text(program_str.text, program_str.x_loc, program_str.y_loc, 1)
        self.display.show()
        
        
class Opt00_str:
    def __init__(self,text,x_loc,y_loc, program):
        self.text = text
        self.x_loc = x_loc
        self.y_loc = y_loc
        self.program = program
#         self.led_status = led.status
    def get_x(self):
        return self.x_loc
    
    def get_y(self):
        return self.y_loc
    
    def str_len(self):
        return len(text)


    def fulltext(self):
        return f"{self.text}"
    





# class Menu_Encoder:
#     def __init__ (self, rot_a_pin, rot_b_pin, rot_sw_pin,selector):
#         self.a = Pin(rot_a_pin, mode = Pin.IN, pull = Pin.PULL_UP)
#         self.b = Pin(rot_b_pin, mode = Pin.IN, pull = Pin.PULL_UP)
#         self.sw = Pin(rot_sw_pin, pull = Pin.PULL_UP, mode = Pin.IN)
#         self.selector = selector
#         self.press_state = 1
#         self.prev_time = 0
# 
#         self.turn_fifo = Fifo(30, typecode = "i") 
#         self.press_fifo = Fifo(30) #default is signed "H"
#         self.a.irq (handler = self.turn_handler, trigger = Pin.IRQ_RISING, hard = True)
#         self.sw.irq(handler = self.press_handler, trigger = Pin.IRQ_RISING, hard = True)
#         self.stop_flag = True
#     
#     def turn_handler(self,pin):
#         #when knob is rotates, check state of b, if b is 1, turn clockwise, if b is 0, turn anti clockwise
#         if self.stop_flag == False:
# #             print("turn here")
#             if self.b():
#                 self.turn_fifo.put(1)
#             else:
#                 self.turn_fifo.put(-1)
#             
#     def press_handler(self,pin):
#         if self.stop_flag == False:
#         
#             cur_time = time.ticks_ms()
#             delta = time.ticks_diff(cur_time, self.prev_time)
#             if delta >= BOUNCE_TIME:
#                 self.press_fifo.put(self.selector.current_pos)
#                 self.prev_time = cur_time

class Opt00_Selector:
    def __init__(self,x_loc,y_loc):
        self.x_loc = x_loc
        self.y_loc = y_loc

        self.str = ""
        self.current_pos = 0
        self.stop_flag = True
        
    def get_select_str(self,program_str):
        return f"{program_str.fulltext()} <-"
    

class Opt00:
    def __init__(self,name,display,encoder,isf_fifo,selector):
        self.name = name
        self.display = display
        self.encoder = encoder
        self.isf_fifo = isf_fifo
        self.selector = selector
        self.current_program = None
        self.program_list = []
        self.stop_flag = True
        self.press = False
        
    def update_selector(self):
        if self.stop_flag == False:
            current_pg_str = self.display.program_str_list[self.selector.current_pos]
            self.selector.str = self.selector.get_select_str(current_pg_str)
            # self.selector.x_loc = get_x_starting(self.selector.str)
            self.selector.x_loc = 0
            self.selector.y_loc = current_pg_str.get_y()
        
    def add_program(self, program):
        self.program_list.append(program)
        
    def turn_encoder(self):
        turn_fifo = self.encoder.t00_fifo
        while turn_fifo.has_data():
            if self.stop_flag == False:
                # turn_fifo = self.encoder.t00_fifo
                start = 0
                end = len(self.display.program_str_list) -1
                direction = turn_fifo.get()
                self.selector.current_pos += direction
                if self.selector.current_pos <= start:
                    self.selector.current_pos = start
                if self.selector.current_pos >= end:
                    self.selector.current_pos = end
            
    def press_encoder(self):
        press_fifo = self.encoder.p00_fifo
        
        while press_fifo.has_data():

            if self.stop_flag == False:
                program_index = press_fifo.get()
                program = self.display.program_str_list[program_index].program
                self.current_program = program
#                 print("current program name ",self.current_program.name)
#                 print(program_index)
                if self.press == True:
                    print(f"program: {self.name} run {program.name}")
#                     program.run()
#                     self.press = False
                self.press = True
#                 self
        
    def run(self):

        if self.stop_flag == False:
            self.update_selector()
            self.display.show_result(self.selector)    
            self.turn_encoder()
            self.press_encoder()
            
    def on(self):
        self.stop_flag = False
        self.display.stop_flag = False
        self.encoder.stop_flag = False
        self.selector.stop_flag = False
        self.encoder.update_program(self)
        self.run()

    def off(self):
        self.press = False
        self.stop_flag = True
        self.display.stop_flag = True
        self.encoder.stop_flag = True
        self.selector.stop_flag = True