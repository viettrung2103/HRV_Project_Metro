from filefifo import Filefifo

data = Filefifo(10, name = '2_capture_250Hz_01.txt')

data_link = []

pre_val = 0
cur_val= 0

pre_slope = 0
cur_slope = 0
count_peak = 0
count = 0
ppi_list = []
count_flag = False

def slope_sign(pre_slope,cur_slope):
    return pre_slope * cur_slope <= 0
            

while data.has_data():
    for _ in range(100):
        value = data.get()
        data_link.append(value)
        
        if _ == 0:
            pre_val = data.get()
            
        elif _ == 1:
            
            cur_val = data.get()
            pre_slope = cur_val - pre_val
        elif _ == 2:
            
            pre_val = cur_val
            cur_val = data.get()
            cur_slope = cur_val - pre_val
        
            
        #actual finding peak and counting
        else:
            #go to peak
            print("cur_slope ",cur_slope)
            print("pre_slope ",pre_slope)
#             print(pre_slope * cur_slope <= 0)
            if slope_sign(pre_slope,cur_slope):
                if pre_slope > 0:
                    if count_flag == False:
                        count_flag = True
                    if count_flag == True:
                        count_flag = False
                
#                 if pre_slope < 0:
#                     count_flag = False
                
                #start counting after count_
            if count_flag == True:
                pre_val = cur_val
                cur_val = data.get()
                pre_slope = cur_slope
                cur_slope = cur_val - pre_val
                count += 1
                
            else:
                pre_val = cur_val
                cur_val = data.get()
                pre_slope = cur_slope
                cur_slope = cur_val - pre_val
                ppi_list.append(count)
#             print(final_list)
#             print(cur_val)
         
        
     