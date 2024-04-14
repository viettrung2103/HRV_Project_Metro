from filefifo import Filefifo
import micropython
micropython.alloc_emergency_exception_buf(200)

number = input("Type number (1-3): ")
filename = f"2_capture_250Hz_0{number}.txt"

data = Filefifo(10, name = filename)

min_val = 0
max_val = 0

def is_greater(max_val,value1):
    if max_val >= value1:
        return max_val
    else:
        return value1
    
def is_smaller(min_val, value1):
    if min_val <= value1:
        return min_val
    else:
        return value1

def convert_value (value,min,max):
    converted = 0
    if value != min:
        converted  = 100 * value / max
    return converted

def find_min_max():
    if data.has_data():
        for _ in range(500):
            value = data.get()
            if _ == 0:
                min = value
                max = value
            else :
                max = is_greater(max,value)
                min = is_smaller(min,value)
    return min, max

min , max = find_min_max()

if data.has_data():
    for _ in range(2500):
        value = data.get()
        converted  = convert_value(value,min,max)
        print(converted)
