import logging
import subprocess
import shlex
import sys, traceback
import os

from PyQt5 import QtCore
from PyQt5.QtCore import QThread, Qt
from PyQt5.QtWidgets import QMessageBox
from GUI.PacketView.WiresharkRunner import WiresharkRunner
from GUI.Dash.RunWebEngine import RunWebEngine

class PacketManager():
    def __init__(self, project_path=None):
        logging.debug('Manager(): Instantiated')
        self.project_path = os.path.abspath(project_path)
        self.filelist = list()
        self.filelist2 = list()
        self.throughput_path = ''
        self.clicks_path = ''
        self.timed_path = ''
        self.wireshark_thread = QThread()
        self.web_engine_thread = QThread()

        try:

            #get dissector files path
            json_path = os.path.join(self.project_path, "ParsedLogs")
            if not os.path.exists(json_path):
                print("NO JSON")
                return
            else:
                for r, d, f in os.walk(json_path):
                        for file in f:
                            if '.JSON' in file:
                                self.filelist2.append(os.path.join(r, file))

            self.runWireshark()

            #get throughput data
            for r, d, f in os.walk(self.project_path):
                for dir in d:
                    #print(dir) 
                    if "ecel-export" in dir:
                        #convert name to string
                        dir = str(dir)
                        self.throughput_path = os.path.join(r, dir)
                        break

            #getting screenshots
            #CLICKS
            self.clicks_path = os.path.join(self.project_path, "Clicks")
            if not os.path.exists(self.clicks_path):
                print("NO SCREENSHOTS")
                return

            #Timed
            self.timed_path = os.path.join(self.project_path, "Timed")
            if not os.path.exists(self.timed_path):
                print("NO Timed SCREENSHOTS")
                return

        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            logging.error('RunWebEngine(): Error during Web Engine termination')
            traceback.print_exception(exc_type, exc_value, exc_traceback)

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
    
    def stopWireshark(self):
        self.wireshark_thread.stopTrigHandle()

    def runWebEngine(self):
        self.web_engine_thread = RunWebEngine()
        self.web_engine_thread.start()
    
    def stopWebEngine(self):
        self.web_engine_thread.stopTrigHandle()
        
    def getJSON(self):
        return self.filelist2
        
    def getThroughput(self):
        return self.throughput_path

    def getClicks(self):
        return self.clicks_path

    def getTimed(self):
        return self.timed_path