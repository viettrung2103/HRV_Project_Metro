from filefifo import Filefifo
data = Filefifo(10, name='capture_250Hz_01.txt')

min_value = float('inf')
max_value = float('-inf')
for _ in range(500): 
    sample = data.get()
    min_value = min(min_value, sample)
    max_value = max(max_value, sample)

for i in range(2500):
    x = data.get()
    y = data.get()
    z = data.get()

    if x < y and z < y:
        y = max_value
    elif x > y and z > y:
        y = min_value

    scaled_value = (y - min_value) / (max_value - min_value)*100
    abbv = round(scaled_value,2)
    print(abbv)

