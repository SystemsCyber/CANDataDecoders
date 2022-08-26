from CANDataSPNDecoder import CANDataSPNDecode
import matplotlib.pyplot as plt
import sys

file = ""
jsonFile = ""
for i, arg in enumerate(sys.argv):
    if(i==1):
        file = arg
    elif(i==2):
        jsonFile = arg

pgn = "61444"
spn = "190"

decodedData = CANDataSPNDecode(file,  jsonFile)
rpmData = decodedData[pgn][spn]["data"]
timeData = decodedData[pgn][spn]["time"]

plt.title(decodedData[pgn][spn]["SPLabel"]) 
plt.xlabel("seconds")
plt.ylabel(decodedData[pgn][spn]["Unit"])
plt.plot(timeData, rpmData)
plt.show()