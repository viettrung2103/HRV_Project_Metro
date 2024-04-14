from filefifo import Filefifo
data = Filefifo(10, name='capture_250Hz_01.txt')

x, y, z = None, None, None 
biggest = 0
sample = 0
PPI = 0
sample_all=0
while data.has_data() and PPI < 3:
    for i in range(100):
        if i % 3 == 0:
            x = data.get()
        elif i % 3 == 1:
            y = data.get()
        elif i % 3 == 2:
            z = data.get()

            if x <= y and z < y:
                biggest += 1
        if biggest == 1 :
            sample +=1
        if biggest ==2:
            print("sample in PPI",PPI+1,":", sample)
            PPI +=1
            biggest = 1
            sample_all += sample
            sample=0
        if PPI == 3:
            print("sample in 3 PPI :", sample_all)
            break
