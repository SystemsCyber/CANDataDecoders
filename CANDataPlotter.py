import sys
import matplotlib.pyplot as plt
from CANDataSPNDecoder import CANDataSPNDecode

#Get User Input
file = ""
jsonFile = ""
for i, arg in enumerate(sys.argv):
    if(i==1):
        file = arg
    elif(i==2):
        jsonFile = arg

#PGN and SPN 
pgn = "61444"
spn = "190"

#Decode candump log File
decodedData = CANDataSPNDecode(file,  jsonFile)
rpmData = decodedData[pgn][spn]["data"]

#Checks if timestamps are in the data
#If not, then it makes the x axis the number of data points
if("time" in decodedData[pgn][spn]):
    timeData = decodedData[pgn][spn]["time"]

#Plot RPM Data
plt.title(decodedData[pgn][spn]["SPLabel"]) 
if("time" in decodedData[pgn][spn]):
    plt.xlabel("seconds")
    plt.plot(timeData, rpmData)
else:
    plt.ylabel(decodedData[pgn][spn]["Unit"])
    plt.plot(rpmData)
plt.show()
