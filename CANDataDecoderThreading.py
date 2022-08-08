import sys
import re
import json
from time import perf_counter
from threading import Thread
from CANDataDecoder import CANDataDecode

def task(data, result, jsonData):
    newDictionary = CANDataDecode(data, jsonData)
    result.update(newDictionary)

result = {}

file = ""
for i, arg in enumerate(sys.argv):
    if(i==1):
        file = arg
    elif(i==2):
        jsonFile = arg
with open(file, "r") as file:
    data = file.read()


#Open and Read J1939 json file
with open(jsonFile, "r") as file:
    jsonData = json.load(file) 

#Split the data and get rid of spaces
if(data[0] == " "):
    data = re.split("\n |\n", data[1:])
else:
    data = re.split("\n |\n", data)        
if(data[len(data)-1] == ""):
    data = data[:len(data)-1]

#Splits the CAN data into 8 sections
data0 = data[:len(data)//8]
data1 = data[len(data)//8:len(data)//4]
data2 = data[len(data)//4:(len(data)//8)*3]
data3 = data[(len(data)//8)*3:len(data)//2]
data4 = data[len(data)//2:(len(data)//8)*5]
data5 = data[(len(data)//8)*5:(len(data)//4)*3]
data6 = data[(len(data)//4)*3:(len(data)//8)*7]
data7 = data[(len(data)//8)*7:]

#Results declare
result0 = {}
result1 = {}
result2 = {}
result3 = {}
result4 = {}
result5 = {}
result6 = {}
result7 = {}

# create threads
t1 = Thread(target=task, args=(data0, result0, jsonData))
t2 = Thread(target=task, args=(data1, result1, jsonData))
t3 = Thread(target=task, args=(data2, result2, jsonData))
t4 = Thread(target=task, args=(data3, result3, jsonData))
t5 = Thread(target=task, args=(data4, result4, jsonData))
t6 = Thread(target=task, args=(data5, result5, jsonData))
t7 = Thread(target=task, args=(data6, result6, jsonData))
t8 = Thread(target=task, args=(data7, result7, jsonData))

# start the threads
t1.start()
t2.start()
t3.start()
t4.start()
t5.start()
t6.start()
t7.start()
t8.start()

# wait for the threads to complete
t1.join()
t2.join()
t3.join()
t4.join()
t5.join()
t6.join()
t7.join()
t8.join()

result.update(result0)
result.update(result1)
result.update(result2)
result.update(result3)
result.update(result4)
result.update(result5)
result.update(result6)
result.update(result7)

with open("CANDataDecoded.json", "w") as outfile:
    outfile.write(json.dumps(result, indent=4))
