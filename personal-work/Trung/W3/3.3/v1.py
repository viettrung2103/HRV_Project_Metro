from filefifo import Filefifo
import micropython
micropython.alloc_emergency_exception_buf(200)



# print("file name: ",file_name)
# value_list  = []
# 
# data = Filefifo(10, name = file_name)
# 
# if data.has_data():
#     for _ in range(1000):
#         value = data.get()
#         value_list.append(value)
# print(len(value_list))

HUNDRED = 100
file_name = "2_capture_250Hz_01.txt"

OLED_W = 128
OLED_H = 64
X_START = 0
X_END = OLED_W - 1
Y_START = 0
Y_END = OLED_H -1


class Program:
    def __init__(self, file_text):
        self.data = Filefifo(10, name = file_name)
        self.data_list = []
        self.converted_list = []
        self.loc_list = []
        self.max = 0
        self.min = 0
        
    def is_larger(self,value):
        if value > self.max:
            return True
    
    def is_smaller(self,value):
        if value < self.min:
            return True
        
    def larger(self,value):
        self.max =  max(self.max, value)
    
    def smaller(self, value):
        self.min =  min(self.min, value)
    
    def find_min_max(self):
        for index, value in enumerate(self.data_list):
            if index == 0:
                self.min = value
                self.max = value
            else:
                if self.is_larger(value):
                    self.larger(value)
                else:
                    self.smaller(value)
        print("max ",self.max)
        print("min ",self.min)
    
    
            
    def save_data_to_list(self):
        if self.data.has_data():
            for _ in range(1000):
                value = self.data.get()
                self.data_list.append(value)
    
    def convert_data(self,value):
        converted_value = 0
        max_delta = self.max - self.min
        if value != self.min:
            value_delta = value - self.min
            converted_value = round(value_delta * HUNDRED / max_delta,0)
        return converted_value
    
    def create_converted_list(self):
        for value in self.data_list:
            converted_data = self.convert_data(value)
            self.converted_list.append(converted_data)
            
    def plot(self):
        for value in self.data_list:
            print(value)
    
    def plot_in_percent(self):
        for value in self.converted_list:
            print(value)
     #when show on screen, it will be inverted       
    def plot_in_led_scale(self):
        for loc in self.loc_list:
            print(loc)
         
        #return x,y
    def convert_to_loc(self,value): # because the y is start from top, not from the bottom
        return  (HUNDRED -value) * Y_END / HUNDRED
    def create_loc_list(self):
        for value in self.converted_list:
            value_loc = self.convert_to_loc(value)
            self.loc_list.append(value_loc)
    
program = Program(file_name)
program.save_data_to_list()
program.find_min_max()
program.create_converted_list()
program.create_loc_list()
# print(program.data_list)
# print(program.converted_list)
# program.plot()
# program.plot_in_percent()
program.plot_in_led_scale()
