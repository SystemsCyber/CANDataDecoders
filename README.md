# CANDataDecoders

These python files are used to decode CAN data and put the results in a json file.

Requires the json file that is generated from J1939toJSON.py in https://github.com/SystemsCyber/J1939Converters. Also requires a copy of the J1939 Digital Annex.

## CANDataDecoder.py
This decoder is used for displaying decoded CAN data. It displays the CAN log message, the pgn label, the spn label, and the value and unit corresponding to each spn. This information is put into a dictionary and then written to a json file called CANDataDecoded.json.

The first argument is for the CAN log file and second argument is the J1939 json file. To run:
```
python3 CANDataDecoder.py example.log J1939DA.json
```
Example of what CANDataDecoded.json could look like:
```
{
    "(000.000000) can1 0CF00400 [8] 11A3A32C32000FA3": {
        "Electronic Engine Controller 1": {
            "Engine Torque Mode": "1.0 nan",
            "Actual Engine - Percent Torque (Fractional)": "0.125 %",
            "Driver's Demand Engine - Percent Torque": "38.0 %",
            "Actual Engine - Percent Torque": "38.0 %",
            "Engine Speed": "1605.5 rpm",
            "Source Address of Controlling Device for Engine Control": "0.0 source address",
            "Engine Starter Mode": "start not requested"
        }
    },
    "(000.005145) can1 18FEDF00 [8] 8AA0287D7DFFFFF5": {
        "Electronic Engine Controller 3": {
            "Nominal Friction - Percent Torque": "13.0 %",
            "Engine's Desired Operating Speed": "1300.0 rpm",
            "Engine's Desired Operating Speed Asymmetry Adjustment": "125.0 nan",
            "Estimated Engine Parasitic Losses - Percent Torque": "0.0 %",
            "Aftertreatment 1 Exhaust Gas Mass Flow Rate": "13107.0 kg/h",
            "Aftertreatment 1 Intake Dew Point": "Not available",
            "Aftertreatment 1 Exhaust Dew Point": "Not available",
            "Aftertreatment 2 Intake Dew Point": "Exceeded the dew point",
            "Aftertreatment 2 Exhaust Dew Point": "Exceeded the dew point"
        }
    },
    ......
}
```

## CANDataSPNDecoder.py
This decoder is used for displaying decoded CAN data. It is similar to CANDataDecoder.py, but it is organized by pgn and spn. This decoder is more ideal for taking specific parts from the CAN data and plotting it. The information is stored in a dictionary and then written to a json file. There is a dictionary with the first pgn. The pgn dictionary contains all of the spns. Within the spn dictionary, the spn label, spn unit, spn data, and spn time is shown. The spn data is a list of all the data and the spn time is a list of all of the time values taken from the CAN log file that correspond to the spn.

The first argument is for the CAN log file and second argument is the J1939 json file. To run:
```
python3 CANDataSPNDecoder.py example.log J1939DA.json
```
Example of what CANDataSPNDecoded.json format (most likely will have a lot more information):
```
{
    "65247": {
        "514": {
            "SPLabel": "Nominal Friction - Percent Torque",
            "Unit": "%",
            "data": [
                13.0,
                13.0,
                13.0,
                14.0
            ],
            "time": [
                0.0,
                0.019846,
                0.039829,
                0.060419
            ]
        },
        "515": {
            "SPLabel": "Engine's Desired Operating Speed",
            "Unit": "rpm",
            "data": [
                1300.0,
                1300.0,
                1300.0,
                1300.0
            ],
            "time": [
                0.0,
                0.019846,
                0.039829,
                0.060419
            ]
        }
    },
    "61444": {
        "190": {
            "SPLabel": "Engine Speed",
            "Unit": "rpm",
            "data": [
                1605.5,
                1611.125,
                1605.5,
                1609.25,
            ],
            "time": [
                0.0,
                0.019846,
                0.039829,
                0.060419
            ]
        }
    }
}
```
This file can be imported and the function CANDataSPNDecode can be used in other python files to plot or manipulate the data. CANDataSPNDecode takes in the CAN log file and the J1939 json file and returns a dictionary with the decoded information. 

Example code of plotting rpm from CAN data using CANDataSPNDecode function:
```
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
```
Example of running:
```
python3 CANDataPlotter.py example.log J1939DA.json 
```

## CANDataDecoderThreading.py
This decoder has the same result as CANDataDecoder.py, but it is used for larger CAN data files that might take too long to decode. It creates 8 threads and splits the CAN Data into 8 sections. It then runs CANDataDecoder.py in each thread and then writes it to CANDataDecoded.json.

The first argument is for the CAN log file and second argument is the J1939 json file. To run:
```
python3 CANDataDecoderThreading.py example.log J1939DA.json
```
