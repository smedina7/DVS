import logging
import subprocess
import shlex
import sys, traceback
import os
from PyQt5 import QtCore
from PyQt5.QtCore import QThread, Qt
from PyQt5.QtWidgets import QMessageBox
from PacketView.WiresharkRunner import WiresharkRunner

class PacketManager():
    def __init__(self, project_path=None):
        logging.debug('Manager(): Instantiated')
        self.project_path = os.path.abspath(project_path)
        self.filelist = list()
        self.filelist2 = list()
        self.wireshark_thread = QThread()

        print(self.project_path)

        #get dissector files path
        json_path = os.path.join(self.project_path, "ParsedLogs")
        print(json_path + " JSON PATH")
        if not os.path.exists(json_path):
            print("NO JSON")
            return
        else:
            for r, d, f in os.walk(json_path):
                    for file in f:
                        if '.JSON' in file:
                            self.filelist2.append(os.path.join(r, file))

        self.runWireshark()
        
    def runWireshark(self):
        #get dissector files path
        dissector_path = os.path.join(self.project_path, "GeneratedDissectors")
        if not os.path.exists(dissector_path):
            print("NO DISSECTORS")
            return
        else:
            for r, d, f in os.walk(dissector_path):
                    for file in f:
                        if '.lua' in file:
                            self.filelist.append(os.path.join(r, file))
                            
        #get pcap file path
        pcap_path = os.path.join(self.project_path, "PCAP/AnnotatedPCAP.pcapng")
        if not os.path.exists(pcap_path):
            print("NO PCAP")
            return

        if len(self.filelist) != 0:
            self.wireshark_thread = WiresharkRunner(lua_scripts =self.filelist, pcap_filename=pcap_path)
        else:
            self.wireshark_thread = WiresharkRunner(pcap_filename=pcap_path)

        self.wireshark_thread.start()

    def getJSON(self):
        return self.filelist2
    