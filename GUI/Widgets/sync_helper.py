import os
import time
from calendar import timegm
from datetime import datetime
import json
import re 
from datetime import datetime, timedelta

class sync_helper:
    def __init__(self):
        pcap_dict = {}

    def get_wireshark_info(project_path):
        tshark_cmd = 'tshark'
        path = project_path + '/GeneratedDissectors/'
        file_list = os.listdir(path)
        for i in file_list:
            tshark_cmd += ' -X lua_script:' + path + i 

        pcap_path = project_path + '/PCAP/'
        tshark_cmd += ' -r ' + pcap_path + 'AnnotatedPCAP.pcapng -T json > ' + pcap_path + '/tshark_out.json'
        os.system(tshark_cmd)
        return pcap_path

    def json_to_dictionary(pcap_path):
        dictionary = {}
        path = pcap_path + '/tshark_out.json'
        with open(path) as json_file: 
            data = json.load(json_file) 
            count = 1
            for i in data:
                source = i.get("_source")
                for k in source:
                    temp = source.get(k)
                    temp2 = re.search(r'[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])T(2[0-3]|[01][0-9]):[0-5][0-9]:[0-5][0-9]', str(temp))
                    if(temp2 is None):
                        dictionary[count]=""
                        count += 1
                    else: 
                        dictionary[count]=temp2.group()
                        count += 1
        return dictionary

    def find_packetnumber(timestamp, dictionary):
        for packet_num, t in dictionary.items():
            if t == timestamp:
                return packet_num
            temp = datetime.strptime(timestamp,'%Y-%m-%dT%H:%M:%S')
            ts_t1 = temp + timedelta(seconds=1)
            ts_1 = datetime.strftime(ts_t1, '%Y-%m-%dT%H:%M:%S')
            if t == ts_1:
                return packet_num

            temp_m = datetime.strptime(timestamp,'%Y-%m-%dT%H:%M:%S')
            ts_t2 = temp + timedelta(seconds=-1)
            ts_2 = datetime.strftime(ts_t2, '%Y-%m-%dT%H:%M:%S')
            if t == ts_2:
                return packet_num


    def write_to_wireshark(packet_num):
        path = os.getcwd()+'/update_wireshark.txt'
        f = open(path,'w+')
        f.write(str(packet_num))
        f.close()
    
    def stop_to_wireshark():
        if(os.path.isfile('update_wireshark.txt')):
            path = os.getcwd()+'/update_wireshark.txt'
            os.remove(path)

    def get_wireshark_click():
        path = os.getcwd()+'/ws_click.txt'
        f = open(path,"r")
        packet_num = str(f.read())
        f.close()
        return int(packet_num)

    def find_timestamp(packet_num, dictionary):
        temp = int(packet_num)
        timestamp = dictionary.get(temp)
        return timestamp



        