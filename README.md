# CANDataDecoders

These python files are used to decode CAN data and put the results in a json file.

Requires the json file that is generated from J1939toJSON.py in SystemsCyber/J1939Converters, which requires a copy of the J1939 Digital Annex.

## CANDataDecoder.py
This decoder is used for displaying decoded CAN data. It displays the CAN log message, the pgn label, the spn label, and the value and unit corresponding to each spn. This information is put into a dictionary and then written to a json file called CANDataDecoded.json.

The first argument is for the CAN log file and second argument is the J1939 json file. To run:
```
python3 CANDataDecoder.py example.log J1939DA.json
```

## CANDataSPNDecoder.py
This decoder is used for displaying decoded CAN data. It is similar to CANDataDecoder.py, but it is organized by pgn and spn. This decoder is more ideal for taking specific parts from the CAN data and plotting it. The information is stored in a dictionary and then written to a json file. There is a dictionary with the first pgn. The pgn dictionary contains all of the spns. Within the spn dictionary, the spn label, spn unit, spn data, and spn time is shown. The spn data is a list of all the data and the spn time is a list of all of the time values taken from the CAN log file that correspond to the spn.

The first argument is for the CAN log file and second argument is the J1939 json file. To run:
```
python3 CANDataSPNDecoder.py example.log J1939DA.json
```

This file can be imported and the function CANDataSPNDecode can be used in other python files to do stuff with the data. CANDataSPNDecode takes in the CAN log file and the J1939 json file and returns a dictionary with the decoded information. 

Example code of plotting rpm from CAN data using CANDataSPNDecode function:
```
from CANDataSPNDecoder import CANDataSPNDecode
import matplotlib.pyplot as plt

decodedData = CANDataSPNDecode("example.log", "J1939DA.json")
rpmData = decodedData["61444"]["190"]["data"]
timeData = decodedData["61444"]["190"]["time"]

plt.title(decodedData["61444"]["190"]["SPLabel"]) 
plt.xlabel("seconds")
plt.ylabel(decodedData["61444"]["190"]["Unit"])
plt.plot(timeData, rpmData)
plt.show()
```

## CANDataDecoderThreading.py
This decoder has the same result as CANDataDecoder.py, but it is used for larger CAN data files that might take too long to decode. It creates 8 threads and splits the CAN Data into 8 sections. It then runs CANDataDecoder.py in each thread and then writes it to CANDataDecoded.json.

The first argument is for the CAN log file and second argument is the J1939 json file. To run:
```
python3 CANDataDecoderThreading.py example.log J1939DA.json
```
