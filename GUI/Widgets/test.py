# import pyshark
# import os

# Open saved trace file 
# cap = pyshark.FileCapture('/ProjectData/t0/PCAP/AnnotatedPCAP.pcapng', only_summaries=True)
# pkts = pyshark.FileCapture(cap)
# print(pkts.get_parameters())
# print (cap[0])
# tshark -r AnnotatedPCAP.pcapng -Y frame.comment -T fields -E header=y -e frame.number -e frame.comment

import json 
import os
from datetime import datetime

command = "tshark -r /home/kali/DVS_dev/ProjectData/t0/PCAP/AnnotatedPCAP.pcapng -Y frame.comment -T fields -E header=y -e frame.number -e frame.comment -e frame.time >> outfile.txt"
os.system(command)

#####OPEN FILE & CREATING DICTIONARY
# List of keys 
# listKeys = ["frame.number", "frame.comment", "scope", "important-packet-identifier","program-used", "cmd", "description" "confidence" ] 
# using zip() function to create a dictionary 
# with keys and same length None value  
# dct = dict(zip(listKeys, [None]*len(listKeys))) 

file = open("outfile.txt")
previous = ""
index = 0
multikeys = []
dct = dict ()

for line in file:
    
    if index != 0:
        # Process the 'line' variable here.
        step_0 = line.split('**')
        print("******************")
        print(step_0)
        print("******************")
        for i in step_0:
            step_1 = i
            step_2 = step_1.split('=')
            # print(step_2)

            fullstring = step_2[0]
            lastitem= (len (step_2)) - 1
            fullstring_two = step_2[lastitem]
            
            substring_one = "\t"
            substring_two = "\n"

            if substring_one in fullstring:
                step_3 = fullstring.split("\t")
                # print ("Found!")
                # print(step_3)
                dct["packet_id"] = step_3 [0]
                dct[step_3[1]]  = step_2[1]
            
            elif substring_one in fullstring_two:
                step_3 = fullstring_two.split("\t")
                # print ("Found!")
                # print(step_3)
                dct[step_2[0]]  = step_3[0]
    
                # "2020-09-02T21:55:21"
                #STEPS to convert timestamp
                temp = step_3[1]
                temp_two = temp.replace('\n','')
                temp_three = temp_two.split('.')
                date_object = datetime.strptime (temp_three[0], '%b %d, %Y %H:%M:%S')
                timestamp = str(date_object)
                timestamp = timestamp.replace(' ','T')
                dct["timestamp"] = timestamp
               
            else:
                dct[step_2[0]]  = step_2[1]

        multikeys.append(dct)
        print("-----------DICT---------")
        print(dct)
        dct = dict ()
    index =  index + 1

file.close()

print("-----------LIST---------")
print(multikeys)

#############################

# Data to be written 
# frame.number	frame.comment
# 6	scope=single**important-packet-identifier=all-packet-payload**program-used=test
# 7	scope=single**important-packet-identifier=all-packet-payload**program-used=test
#10	scope=single**important-packet-identifier=all-packet-payload**program-used=this program**cmd=this command**description=this description**confidence=2
# dictionary ={ 
#     "frame.number" : 6, 
#     "frame.comment" : "scope=single**important-packet-identifier=all-packet-payload**program-used=test", 
#     "scope" : "single", 
#     "important-packet-identifier" : "all-packet-payload",
#     "program-used" : "test",
#     "cmd" : "this command",
#     "description" : "this description",
#     "confidence" : "2"

# } 

# Serializing json  
json_object = json.dumps(multikeys, indent = 4) 
  
# Writing to sample.json 
with open("sample.json", "w") as outfile: 
    outfile.write(json_object) 