from filefifo import Filefifo
import micropython
micropython.alloc_emergency_exception_buf(200)

number = input("Type 1-3 for file name: ")
# number = 1
file_name = f"2_capture_250Hz_0{number}.txt"
print("file name: ",file_name)

data = Filefifo(10, name = file_name)
count = 0 # to count amount of sampler btwn 2 peak
count_peak = 0 #  < <= 4 >> to get 3 ppi
delta = 0.004

sum = 0
# cur_sum = 0

pre_mean = 0
cur_mean = 0

pre_slp = 0
cur_slp = 0

count_peak = 0

n = 2 # number of sample for mean
# count_peak = 0
count_flag = False
count_list = []

def is_peak(pre_slp,cur_slp):
    if pre_slp < 0 and cur_slp >= 0:
        return True
    else:
        return False
        
def find_mean_count_and_time(count_list):
    total = 0
    for value in count_list:
        total += value
    mean = int(round(total / len(count_list),0))
    total_time = mean * delta
    return mean, total_time

def find_mean_time(mean_count):
    total = 0
    for value in count_list:
        total += value
    return total * delta

def find_frequency(time):
    frequency = 1/time
    return round(frequency,2)

def display_result(count_list):
    for i in count_list:
        print(i)
    count, total_time = find_mean_count_and_time(count_list)
    frequency = find_frequency(total_time)
    print(f"""samples: {count}
time: {total_time:.3f}
frequency: {frequency}
                """)

# while data.has_data() and len(count_list) < 3:
while data.has_data() and len(count_list) < 3:
    for _ in range(1000):
        value = data.get()
        #setting  value for pre_mean
        if _ <= n:
            sum += value
            if _ == n:
                pre_mean = round(sum / n)
                sum = 0   
        # setting value for cur_mean, pre_slp       
        elif n < _ and _ <= 2 * n:
            sum += value
            if _ % n == 0:
               cur_mean = round(sum / n,2)
               per_slp = cur_mean-pre_mean
               sum = 0
        #setting value cur_slp   
        elif 2 * n < _ and _ <= 3 * n:
            sum += value
            if _ % n == 0:
                pre_mean = cur_mean
                cur_mean = round(sum / n,2)
                cur_slp = cur_mean - pre_mean
                sum = 0
        else:
            # start polling
            sum += value
            if _ % n == 0:
                if count_flag == True:
                    pre_mean = cur_mean
                    cur_mean = round(sum / n,2)
                    pre_slp = cur_slp
                    cur_slp = cur_mean - pre_mean
                    sum = 0
                else:
                    pre_mean = cur_mean
                    cur_mean = round(sum / n,2)
                    pre_slp = cur_slp
                    cur_slp = cur_mean - pre_mean
                    sum = 0     
                # find peak
#                 if is_peak(pre_slp,cur_slp) and pre_slp > 0 and len(count_list) <3:
#                 if is_peak(pre_slp,cur_slp) and count_peak <= 4:
                if is_peak(pre_slp,cur_slp) and len(count_list) <3:
#                 if slope_sign(pre_slp,cur_slp) and count_peak < 2 and len(count_list) <3:
#                     count_peak += 1
                    #start count peak from the first peak
                    count_peak += 1
                    if count_flag == False:
                        count_flag = True
                    # start from peak 2    
                    else:
#                         count_flag = False
                        if count != 0:
#                         if count != 0 and count_peak == 2 :
                            count_list.append(count)
                            count = 0
#                             count_peak = 0
                            
        if count_flag == True:
            count += 1
            
display_result(count_list)
                        
        
                
#         print(value)
#         print("cur",cur_mean)
        
        
           
        