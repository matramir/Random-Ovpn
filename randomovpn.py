#! python3
# randomovpn.py - script that connects you to a random openvpn server using the linux terminal
# usage:Type "python3 randomovpn.py" inside the openvpn folder as your present working directory
# type tcp or udp to select type of connection
# select country or type random to select a random country
import random, os, re, subprocess, sys, pprint

#asks for the server protocol that the user wants to connect
print("Please select TCP or UDP as your protocol, type 'exit' to exit the program")
protocol=""
protocolFolder=""
while True:
    pt=input()
    if pt in ("TCP", "tcp"):
        protocol="tcp"
        protocolFolder = 'ovpn_tcp'
        break
    elif pt in ("UDP", "udp"):
        protocol="udp"
        protocolFolder = 'ovpn_udp'
        break
    elif pt == "exit":
        sys.exit()
    else:
        print("Please try again, you have not selected neither TCP or UDP as a protocol")

#generate a list of files inside the specified protocol folder
fileList=[]
dirPath = os.path.abspath(os.path.join('.', protocolFolder))
for folderName, subfolder, filename in os.walk(dirPath):
    fileList=filename

#Generate a list of possible countries and servers
countryList=[]
serverDict={}
serverRegex = re.compile(r'''(
([a-z]+) # country
(\d+) # server number
(.nordvpn.com.tcp.ovpn|.nordvpn.com.udp.ovpn) # rest of the server domain
)''', re.VERBOSE)

for file in fileList:
    sm = serverRegex.search(file)
    country = sm.group(2)
    serverN = sm.group(3)
    if country not in countryList:
        countryList.append(country)
        serverDict[country]=[]
    serverDict[country].append(str(serverN))
# country selection
selectedCountry=''
while True:
    print("Select a country. To see the country list type \"list\"")
    ct = input()
    if ct ==  'list':
        pprint.pprint(countryList)
    elif ct in countryList:
        selectedCountry = ct
        break
    else:
        print("Please enter a valid country")
#server connection
selectedServer = (selectedCountry+(random.choice(serverDict[selectedCountry])))+".nordvpn.com."+protocol+".ovpn"
print("Connecting to "+selectedServer)
serverPath = os.path.abspath(os.path.join('.', protocolFolder,selectedServer))
command = "/usr/sbin/openvpn"
subprocess.call(["sudo", command, serverPath])
