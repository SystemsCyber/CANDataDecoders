import re
import json
import sys

def CANDataSPNDecode(file):
    #Open and read CAN data file
    with open(file, "r") as file:
        data = file.read()

    #Open and Read J1939 json file
    with open("J1939DA_MAY2022.json", "r") as jsonFile:
        jsonData = json.load(jsonFile) 

    #Split the data and get rid of spaces
    if(data[0] == " "):
        organizedData = re.split("\n |\n", data[1:])
    else:
        organizedData = re.split("\n |\n", data)
    organizedData = organizedData[:len(organizedData)-1]

    #Declare dictionary that will be returned
    returnJson = {}

    #Declare lists
    time = []
    dataID = []
    byteData = []
    numOfBytes= []
    CANData = []

    #Parses CAN data into four lists, which are time, ID, data bytes, and byte data length
    for i in range(0, len(organizedData)):
        split = re.split("   |  ", organizedData[i])

        time.append(split[0][1:len(split[0])-1])
        dataID.append(split[2])
        numOfBytes.append(split[3][1:2])
        byteData.append(split[4])

        bytesCombined = ""
        splitbytes = split[4].split(" ")
        for i in range(0, len(splitbytes)):
            bytesCombined = bytesCombined + splitbytes[i]


        CANData.append(split[0] + " " + split[1] + " " + split[2] + " " + split[3] + " " + bytesCombined)

    #Analyze CAN data
    for i in range(0, len(dataID)):

        #Checks byte amount
        if(len(dataID[i]) < 8):
            continue

        #Calculate PGN
        pgn = dataID[i][2:6]
        if(int(pgn[0:2],16) < int("F0",16)):
            pgn = pgn[0:2] + "00"
        pgn = str(int(pgn, 16))

        #Combine the data bytes into one string
        bytesList = byteData[i].split(" ")
        if(len(bytesList) < 8):
            continue
        bytesString = bytesList[0] + bytesList[1] + bytesList[2] + bytesList[3] + bytesList[4] + bytesList[5]+ bytesList[6] + bytesList[7]

        #Load in data, time, unit, and SP Labels into returnFile dictionary
        if(pgn in returnJson):

            #If the pgn is in the dictionary, then just append the SPN data into the corresponding lists in the dictionary
            try:
                spnList = jsonData["PGN"][pgn]["SPN"]
            except KeyError:
                continue
            startBit = jsonData["PGN"][pgn]["SPNStartBit"]
            for j in range(0, len(spnList)):

                #Splits the spLength into two strings. One is the value and other is a unit
                spLength = jsonData["SPN"][spnList[j]]["SP Length"].split(" ")

                #Case for if spLength does not exist
                if(spLength == ["nan"]):
                    continue

                #Creates bitLength variable and adds amount of bits into it based on if the unit is byte or bit
                bitLength = 1
                if(spLength[1] == "bytes" or spLength[1] == "byte"):
                    bitLength = int(spLength[0]) * 8
                elif(spLength[1] == "bits" or spLength[1] == "bit"):
                    bitLength = int(spLength[0])


                #Gets the start bit into a better value for accessing a specific part of the binary value of the data
                splitStartBit = startBit[j].split(".")
                SPNStartBit = (int(splitStartBit[0])-1)*8 + (int(splitStartBit[1])-1)

                #Creates binary value of data
                val = bin(int(bytesString, 16))[2:].zfill(64)

                #Case for if val is empty
                if(val == ""):
                    continue

                #Checks if it is in bits, if so, then calculate data and append lists
                if(spLength[1] == "bits" or spLength[1] == "bit"):
                    data = int(val[SPNStartBit:SPNStartBit+bitLength]) *float(jsonData["SPN"][spnList[j]]["Scale (Value Only)"]) +float(jsonData["SPN"][spnList[j]]["Offset (Value Only)"])
                    returnJson[pgn][spnList[j]]["data"].append(int(data))
                    returnJson[pgn][spnList[j]]["time"].append(float(time[i]))
                    continue


                #Parse the binary value into the specific SPN data range
                binaryData = val[SPNStartBit:SPNStartBit+bitLength]

                dataRangeBinary = ""

                #If it is in bytes, then read the bytes in reverse
                for z in range(0, int(spLength[0])):
                    dataRangeBinary += binaryData[(len(binaryData)-8*z-8):(len(binaryData)-8*z)]


                #Calculate Data
                data = int(dataRangeBinary,2) *float(jsonData["SPN"][spnList[j]]["Scale (Value Only)"]) +float(jsonData["SPN"][spnList[j]]["Offset (Value Only)"])

                if(float(jsonData["SPN"][spnList[j]]["Offset (Value Only)"]) <= data <= float(jsonData["SPN"][spnList[j]]["RangeMax (Value Only)"])):
                    returnJson[pgn][spnList[j]]["data"].append(data)
                    returnJson[pgn][spnList[j]]["time"].append(float(time[i]))

        else:
            #If the pgn is not in the dictionary, then add it into the dictionary and declare the SPNs and add in data into lists
            try:
                spnList = jsonData["PGN"][pgn]["SPN"]
            except KeyError:
                continue
            startBit = jsonData["PGN"][pgn]["SPNStartBit"]
            returnJson[pgn] = {}

            #Loop for going through SPNs corresponding to the PGN
            for j in range(0, len(spnList)):
                #Make a dictionary for each SPN
                returnJson[pgn][spnList[j]] = {}
                returnJson[pgn][spnList[j]]["SPLabel"] = jsonData["SPN"][spnList[j]]["SP Label"]
                returnJson[pgn][spnList[j]]["Unit"] = jsonData["SPN"][spnList[j]]["Unit"]
                returnJson[pgn][spnList[j]]["data"] = []
                returnJson[pgn][spnList[j]]["time"] = []



                #Splits the spLength into two strings. One is the value and other is a unit
                spLength = jsonData["SPN"][spnList[j]]["SP Length"].split(" ")

                #Case for if spLength does not exist
                if(spLength == ["nan"]):
                    continue

                #Creates bitLength variable and adds amount of bits into it based on if the unit is byte or bit
                bitLength = 1
                if(spLength[1] == "bytes" or spLength[1] == "byte"):
                    bitLength = int(spLength[0]) * 8
                elif(spLength[1] == "bits" or spLength[1] == "bit"):
                    bitLength = int(spLength[0])


                #Gets the start bit into a better value for accessing a specific part of the binary value of the data
                splitStartBit = startBit[j].split(".")
                SPNStartBit = (int(splitStartBit[0])-1)*8 + (int(splitStartBit[1])-1)


                #Creates binary value of data
                val = bin(int(bytesString, 16))[2:].zfill(64)

                #Case for if val is empty
                if(val == ""):
                    continue

                #Checks if it is in bits, if so, then calculate data and append lists
                if(spLength[1] == "bits" or spLength[1] == "bit"):
                    data = int(val[SPNStartBit:SPNStartBit+bitLength]) *float(jsonData["SPN"][spnList[j]]["Scale (Value Only)"]) +float(jsonData["SPN"][spnList[j]]["Offset (Value Only)"])
                    returnJson[pgn][spnList[j]]["data"].append(int(data))
                    returnJson[pgn][spnList[j]]["time"].append(float(time[i]))
                    continue

                #Parse the binary value into the specific SPN data range
                binaryData = val[SPNStartBit:SPNStartBit+bitLength]

                dataRangeBinary = ""

                #If it is in bytes, then read the bytes in reverse
                for z in range(0, int(spLength[0])):
                    dataRangeBinary += binaryData[(len(binaryData)-8*z-8):(len(binaryData)-8*z)]

                #Calculate data
                data = int(dataRangeBinary,2) *float(jsonData["SPN"][spnList[j]]["Scale (Value Only)"]) +float(jsonData["SPN"][spnList[j]]["Offset (Value Only)"])

                if(float(jsonData["SPN"][spnList[j]]["Offset (Value Only)"]) <= data <= float(jsonData["SPN"][spnList[j]]["RangeMax (Value Only)"])):
                    returnJson[pgn][spnList[j]]["data"].append(data)
                    returnJson[pgn][spnList[j]]["time"].append(float(time[i]))

    return returnJson

if __name__ == '__main__':
    file = ""
    for i, arg in enumerate(sys.argv):
        if(i==1):
            file = arg
    decoded = CANDataSPNDecode(file)

    with open("CANDataSPNDecoded.json", "w") as outfile:
        outfile.write(json.dumps(decoded, indent=4))