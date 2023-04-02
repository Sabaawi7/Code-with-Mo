import subprocess as sp
import xml.etree.cElementTree as ET
from os import listdir
import pandas as pd
from time import sleep

print("Program started...")
sleep(1)
print("Collecting Data...")
sleep(3)

# Executing the Windows commands while hiding the outputs
sp.call("mkdir WifiData", shell=True, stdout=sp.DEVNULL,
    stderr=sp.STDOUT)
sp.call("netsh wlan export profile key=clear",cwd="WifiData" ,shell= True, stdout=sp.DEVNULL,
    stderr=sp.STDOUT)

print("Almost Done...")

sleep(2)

# Creating Container for WifiData
WifiList = []

# Parsing through every File and filling the List above with data
for file in listdir("WifiData"):
    myTree = ET.parse(f"WifiData\{str(file)}")
    myRoot = myTree.getroot()
    
    SSID = myRoot[0].text
    Auth = myRoot[4][0][0][0].text
    if Auth != "open":
        Password = myRoot[4][0][1][2].text
    else:
        Password = "None"
    WifiDict = {
        "Name": SSID,
        "Auth": Auth,
        "Password": Password
    }
    WifiList.append(WifiDict)

# Export WifiData to an HTML File
df = pd.DataFrame.from_dict(WifiList)
df.to_html("WifiData.html")

print("Done!")
