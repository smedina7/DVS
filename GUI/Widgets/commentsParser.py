import json 
import os.path
import sys
from datetime import datetime


class commentsParser:
    def __init__(self, path): 

        if sys.platform == "linux" or sys.platform == "linux2":  
            pcappath = path + "/PCAP/AnnotatedPCAP.pcapng"

        else:
            pcappath = path + "\\PCAP\\AnnotatedPCAP.pcapng"

        file_path = os.path.abspath("GUI/Widgets/pcomments.txt")
        # file_path = "/home/kali/DVS_dev/GUI/Widgets/pcomments.txt"
        if os.path.isfile(file_path):
            file = open(file_path,"r+")
            file.truncate(0)
            
            command = "tshark -r " + pcappath + " -Y frame.comment -T fields -E header=y -e frame.number -e frame.comment -e frame.time >> " + file_path
            os.system(command)

        else:
            command = "tshark -r " + pcappath + " -Y frame.comment -T fields -E header=y -e frame.number -e frame.comment -e frame.time >> " + file_path
            os.system(command)
            file = open(file_path,"r+")





        #####OPEN FILE & CREATING DICTIONARY


        # Define List of keys/columns 
        listKeys = ["packet_id", "scope", "important-packet-identifier","program-used", "cmd", "description", "confidence","timestamp" ] 
        # listKeys = ["packet_id", "scope", "important-packet-identifier","program-used", "cmd", "description", "confidence","advanced", "customSuricataRule","timestamp" ] 



        num_lines = sum(1 for line in open(file_path))
        print(num_lines)

        index = 0
        multikeys = []
        dct = dict ()

        if num_lines < 2:
            dct = dict(zip(listKeys, [None]*len(listKeys))) 
            multikeys.append(dct)

        else: 

            with open(file_path) as file_in:
                for line in file:
                    # using zip() function to create a dictionary 
                    # with keys and same length None value  
                    dct = dict(zip(listKeys, [None]*len(listKeys))) 
                    
                    if index != 0:
                        # Process the 'line' variable here.
                        step_0 = line.split('**')

                        for i in step_0:
                            step_1 = i
                            step_2 = step_1.split('=')

                            fullstring = step_2[0]
                            lastitem= (len (step_2)) - 1
                            fullstring_two = step_2[lastitem]
                            
                            substring_one = "\t"
                            substring_two = "\n"

                            if substring_one in fullstring:
                                step_3 = fullstring.split("\t")
                                dct["packet_id"] = step_3 [0]
                                dct[step_3[1]]  = step_2[1]
                            
                            elif substring_one in fullstring_two:
                                step_3 = fullstring_two.split("\t")
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
                        # print("-----------DICT---------")
                        # print(dct)
                        dct = dict ()
                    index =  index + 1
            

        file.close()


        # print("-----------LIST---------")
        # print(multikeys)

        #############################

        # Data to be written 
        # Serializing json  
        json_object = json.dumps(multikeys, indent = 4) 
        # print(path)

        if sys.platform == "linux" or sys.platform == "linux2":  
            jsonpath = path + "/ParsedLogs/pcomments.json"
        else:
            jsonpath = path + "\\ParsedLogs\\pcomments.json"

        with open(jsonpath, "w") as outfile: 
            outfile.write(json_object) 

