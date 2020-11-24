import json
import os.path
import sys
from datetime import datetime


class commentsParser:
    def __init__(self, path):
        self.pcappath = path + "/PCAP/AnnotatedPCAP.pcapng"
        self.comments_path = os.path.abspath("GUI/Widgets/pcomments.txt")
        self.multikeys = []
        self.listKeys = ["packet_id", "scope", "important-packet-identifier", "program-used", "cmd", "description",
                         "confidence", "timestamp"]

        self.extractComments(self.pcappath)
        self.generateJSON(self.comments_path, path)

    def extractComments(self, pcappath):
        cmd = "tshark -r "
        cmd += pcappath
        cmd += " -Y frame.comment -T fields -E header=y -e frame.number -e frame.comment -e frame.time > "
        cmd += self.comments_path

        os.system(cmd)

    def generateJSON(self, file, path):

        num_lines = sum(1 for line in open(file))

        if num_lines < 2:
            dct = dict()
            dct = dict(zip(self.listKeys, ["No data"] * len(self.listKeys)))
            self.multikeys.append(dct)
            print(self.multikeys)
        else:
            index = 0
            dct = dict()
            with open(file) as file_in:
                for line in file_in:
                    if line.split('\t')[0] == "frame.number":
                        pass
                    else:
                        step_0 = line.split('**')
                        for i in step_0:
                            step_1 = i
                            step_2 = step_1.split('=')

                            fullstring = step_2[0]
                            lastitem = (len(step_2)) - 1
                            fullstring_two = step_2[lastitem]
                            substring_one = "\t"
                            substring_two = "\n"

                            if substring_one in fullstring:
                                step_3 = fullstring.split("\t")
                                # print(step_3)
                                dct["packet_id"] = step_3[0]
                                dct[step_3[1]] = step_2[1]

                                print(dct["packet_id"])

                            elif substring_one in fullstring_two:
                                step_3 = fullstring_two.split("\t")
                                dct[step_2[0]] = step_3[0]

                                # "2020-09-02T21:55:21"
                                # STEPS to convert timestamp
                                temp = step_3[1]
                                temp_two = temp.replace('\n', '')
                                temp_three = temp_two.split('.')
                                date_object = datetime.strptime(temp_three[0], '%b %d, %Y %H:%M:%S')
                                timestamp = str(date_object)
                                timestamp = timestamp.replace(' ', 'T')
                                dct["timestamp"] = timestamp

                            else:
                                dct[step_2[0]] = step_2[1]

                        self.multikeys.append(dct)
                        dct = dict()
                    index = index + 1

        json_object = json.dumps(self.multikeys, indent=4)
        if sys.platform == "linux" or sys.platform == "linux2":
            jsonpath = path + "/ParsedLogs/pcomments.json"
        
        else:
            jsonpath = path + "\\ParsedLogs\\pcomments.json"

        with open(jsonpath, 'w') as outfile:
            outfile.write(json_object)
