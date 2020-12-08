import logging
import os
import time
from re import search
import subprocess
import json
import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWebEngineWidgets import *
from GUI.Widgets.textdataline import TextDataline, reloadDataline
from GUI.Widgets.Mouseclicks import First
from GUI.Widgets.TimedScreenshots import Timed
import pandas as pd
from GUI.Widgets.Timestamp import Timestamp
from GUI.Widgets.sync_helper import sync_helper
from GUI.PacketView.WiresharkColorFilters import WiresharkColors, clearFilters
from GUI.Threading.BatchThread import BatchThread
from GUI.Dialogs.ProgressBarDialog import ProgressBarDialog
from GUI.Dialogs.ExportDialog import ExportDialog
from GUI.Dialogs.EditTextDialog import EditTextDialog
from GUI.Dialogs.DateTimePicker import DateTimePicker
from GUI.Dialogs.AddTag import AddTagDialog
import time
import datetime

#PARSER
from GUI.Widgets.commentsParser import commentsParser
#SAVE
from GUI.Widgets.save import save

class MainGUI(QMainWindow):
    #Signal for when the user wants to create a new project
    new_import = QtCore.pyqtSignal(bool)
    #Signal for when the user wants to open previous project
    open_prev = QtCore.pyqtSignal(bool)

    def __init__(self, json_files, clicks, timed, throughput, manager_inst, parent = None):
        logging.debug("MainGUI(): Instantiated")
        super(MainGUI, self).__init__(parent)
        json_file_list = json_files
        self.clicks_path = clicks
        self.timed_path = timed
        self.manager_instance = manager_inst
        throughput_path = throughput
        self.web = ''
        self.progress = ProgressBarDialog(self, 100)
        t = Timestamp()
        self.project_path = os.path.dirname(clicks)
        self.throughput_open1 = False
        self.ProjectFolder = throughput.rsplit('/', 1)
        self.PCAPpath = self.ProjectFolder[0] + "/PCAP/AnnotatedPCAP.pcapng"

        self.key_json = ''
        self.sys_json = ''
        self.mouse_json = ''
        self.timed_json = ''
        self.suricata_json = ''
        self.throughput_json = throughput_path + '/parsed/tshark/networkDataXY.JSON'

        self.project_name = os.path.basename(self.project_path)
        self.subK = QMdiSubWindow()
        self.subSC = QMdiSubWindow()
        self.subT = QMdiSubWindow()
        self.subM = QMdiSubWindow()

        self.project_dict = {}
        self.project_dict[self.project_name] = {"KeypressData": {}, "SystemCallsData": {}, "MouseClicksData": {}, "TimedData": {}, "ThroughputData": {}, "SuricataData": {}}

        #Get JSON Files        
        #get path for each file
        for file in json_file_list:
            if "Keypresses.JSON" in file:
                self.key_json = file
            
            if "SystemCalls.JSON" in file:
                self.sys_json = file
            
            if "MouseClicks.JSON" in file:
                self.mouse_json = file
            
            if "TimedScreenshots.JSON" in file:
                self.timed_json = file

        #Create toolbar and sync button widgets
        self.tb = self.addToolBar("")
        # Wireshark sync button
        self.sync_button_wireshark = QPushButton(self.tb)
        self.sync_button_wireshark.setCheckable(True)
        self.sync_button_wireshark.setText("Wireshark Sync : off")
        self.sync_button_wireshark.setEnabled(False)
        self.sync_button_wireshark.setStyleSheet("QPushButton {background-color: rgb(156,145,145); color: gray;}")
        self.tb.addWidget(self.sync_button_wireshark)
        self.sync_button_wireshark.clicked.connect(self.buttonaction_wireshark)

        # Timestamp sync button
        self.sync_button_timestamp = QPushButton(self.tb)
        self.sync_button_timestamp.setCheckable(True)
        self.sync_button_timestamp.setText("Timestamp Sync: off")
        self.tb.addWidget(self.sync_button_timestamp)
        self.sync_button_timestamp.clicked.connect(self.buttonaction_timestamp)

        #Refresh button for comments packets
        self.refresh = QPushButton (self.tb)
        self.refresh.setText("Refresh Comments Dataline")
        self.tb.addWidget(self.refresh)
        self.refresh.clicked.connect (self.trigger_refresh)

        ##SAVE
        self.save = QPushButton('SAVE')
        self.save.setFixedWidth(100)
        self.tb.addWidget(self.save)
        self.save.clicked.connect(self.saveDataline)

        #Set area for where datalines are going to show
        self.mdi = QMdiArea()
        self.setCentralWidget(self.mdi)
        self.mdi.setAttribute(QtCore.Qt.WA_DeleteOnClose, False)

        #add scrollbar
        self.mdi.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.mdi.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        #Add menu bar
        bar = self.menuBar()
        file = bar.addMenu("File")
        save = file.addAction("Save")
        importProject = file.addAction("New Project/Import")
        openPrevProject = file.addAction("Open Previous")
        exportProject = file.addAction("Export")
        quitDVS = file.addAction("Quit")

        quitDVS.triggered.connect(self.closeEvent)
        exportProject.triggered.connect(self.export_project)
        importProject.triggered.connect(self.new_import_project)
        openPrevProject.triggered.connect(self.open_prev_project)

        #add default datalines
        add_dataline = bar.addMenu("Add Dataline")
        preset_dataline = add_dataline.addMenu("Preset Dataline")
        custom_dataline = add_dataline.addAction("Choose JSON")

        self.throughput = preset_dataline.addAction("Throughput")
        self.keypress = preset_dataline.addAction("Keypresses")
        self.syscalls = preset_dataline.addAction("System Calls")
        self.mouse = preset_dataline.addAction("Mouse Clicks")
        self.timed = preset_dataline.addAction("Timed Screenshots")

        self.throughput.setCheckable(True)
        self.keypress.setCheckable(True)
        self.syscalls.setCheckable(True)
        self.mouse.setCheckable(True)
        self.timed.setCheckable(True)
        
        #dataline windows actions
        self.throughput.triggered.connect(self.throughput_selected)
        self.resizeEvent(self.throughput.triggered)
        self.keypress.triggered.connect(self.keypresses_selected)
        self.resizeEvent(self.keypress.triggered)
        self.syscalls.triggered.connect(self.syscalls_selected)
        self.resizeEvent(self.syscalls.triggered)
        self.mouse.triggered.connect(self.mouse_selected)
        self.resizeEvent(self.mouse.triggered)
        self.timed.triggered.connect(self.timed_selected)
        self.resizeEvent(self.timed.triggered)

        custom_dataline.triggered.connect(self.choose_json)
        self.resizeEvent(custom_dataline.triggered)

        adjust = bar.addMenu("Adjust Subwindows")
        adjust.addAction("Tile Layout")
        adjust.triggered[QAction].connect(self.tile_selected)

        #Home Window Widget Configuration
        window_title = "Timeline View - " + self.project_name
        self.setWindowTitle(window_title)
        self.setMinimumHeight(750)
        self.setMinimumWidth(850)
        # sync stuff
        self.timestamp = ""
        self.timestampTrigger = False
        self.wiresharkTrigger = False
        self.sync_dict = {}

    def file_changed(self):
        self.syncWindows(1)

    def wire_to_DVS(self):
        if(self.wiresharkTrigger == True):
            time.sleep(0.5)
            packet_num = sync_helper.get_wireshark_click()
            dictionary_temp = self.sync_dict
            timestamp_w = sync_helper.find_timestamp(packet_num,dictionary_temp)
            if not timestamp_w == "":
                Timestamp.update_timestamp(str(timestamp_w))

    def buttonaction_wireshark(self, b):
        if b == True:
            self.sync_button_wireshark.setText("Wireshark Sync : on")
            self.wiresharkTrigger = True
            p_path = self.project_path
            pcap_path = sync_helper.get_wireshark_info(p_path)
            dictionary = sync_helper.json_to_dictionary(pcap_path)
            self.sync_dict = dictionary

        else:
            self.sync_button_wireshark.setText("Wireshark Sync : off")
            self.wiresharkTrigger = False

    def syncWindows(self, b):
        if self.timestampTrigger:
            children = self.findChildren(QTableWidget)
            for child in children:
                columncount = child.columnCount()
                for row in range(child.rowCount()):
                    for col in range (child.columnCount()):
                        child.item(row, col).setBackground(QtGui.QColor(255, 255, 255, 0))

                for row in range(child.rowCount()):
                    indexTimeStamp = child.item(row,columncount-1).text()
                    if b == -1:
                        if self.timestamp == indexTimeStamp:
                            for col in range (child.columnCount()):
                                child.item(row, col).setBackground(QtGui.QColor(125,125,125))
                            Timestamp.update_timestamp(self.timestamp)#writes to timestamp.txt
                    else:
                        currTimeStamp = Timestamp.get_current_timestamp()#reads timestamp.txt
                        if indexTimeStamp == currTimeStamp:
                            for col in range (child.columnCount()):
                                child.item(row, col).setBackground(QtGui.QColor(125,125,125))

        if self.timestampTrigger == False:
            children = self.findChildren(QTableWidget)
            for child in children:
                for row in range(child.rowCount()):
                    for col in range (child.columnCount()):
                        child.item(row, col).setBackground(QtGui.QColor(255, 255, 255, 0))
        
        if self.wiresharkTrigger == True:
            dictionary = self.sync_dict  
            timestamp = Timestamp.get_current_timestamp()
            packet_num = sync_helper.find_packetnumber(timestamp, dictionary)
            sync_helper.write_to_wireshark(packet_num)

        if self.wiresharkTrigger == False:
            sync_helper.stop_to_wireshark()

    def buttonaction_timestamp(self, b):
        if b == True:
            self.sync_button_timestamp.setText("Timestamp Sync : on")
            self.timestampTrigger = True
            self.sync_button_wireshark.setEnabled(True)
            self.sync_button_wireshark.setStyleSheet("QPushButton {background-color: #353535}")
            self.file_watcher = QFileSystemWatcher()
            ts_path = os.path.abspath("GUI/Dash/timestamp.txt")
            self.file_watcher.addPath(ts_path) #listens for file changes
            self.file_watcher.fileChanged.connect(self.file_changed)
            path = os.getcwd()+'/ws_click.txt'
            self.ws_watcher = QFileSystemWatcher()
            self.ws_watcher.addPath(path) #listens for file changes
            self.ws_watcher.fileChanged.connect(self.wire_to_DVS)
            # redraw
            self.syncWindows(-1)
        else:
            self.sync_button_timestamp.setText("Timestamp Sync : off")
            self.timestampTrigger = False
            self.sync_button_wireshark.setText("Wireshark Sync : off")
            self.sync_button_wireshark.setEnabled(False)
            self.sync_button_wireshark.setStyleSheet("QPushButton {background-color: rgb(156,145,145); color: gray;}")
            self.wiresharkTrigger = False
            # undraw
            self.timestamp = ""
            self.syncWindows(-1)

    def resizeEvent(self, event):
        self.sizeHint()

    def getCoords(self, r , c):
        sender = self.sender()
        name = sender.objectName()
        table = self.findChild(QTableWidget, name)
        columncount = table.columnCount()
        indexTimeStamp = table.item(r,columncount-1).text()
        if (self.timestampTrigger):
            self.timestamp = indexTimeStamp
            Timestamp.update_timestamp(self.timestamp) #writes to timestamp.txt (updates timestamp)
            self.syncWindows(-1)

    def table_clicked(self, cell_obj):
        sender = self.sender()
        name = sender.objectName()
        table = self.findChild(QTableWidget, name)
        current_timestamp = table.item(cell_obj.row(), cell_obj.column()).text()
        columnname = "content"
        headercount = table.columnCount()
        row = table.currentItem().row()

        if cell_obj.column() == table.columnCount()-1:
            datepicker = DateTimePicker()
            timestamp = datepicker.get_timestamp()
            if not len(timestamp) == 1:
                table.setItem(cell_obj.row(), cell_obj.column(), QTableWidgetItem(timestamp))
            else:
                table.setItem(cell_obj.row(), cell_obj.column(), QTableWidgetItem(current_timestamp))
            table.item(cell_obj.row(), cell_obj.column()).setFlags(QtCore.Qt.ItemIsEnabled)

        else:
            for x in range(0,headercount,1):
                headertext = table.horizontalHeaderItem(x).text()
                if columnname == headertext:
                    cell_text = table.item(row, x).text()   # get cell at row, col
                    self.trigger_edit(cell_text, table, row, x)
                else:
                    pass

    def selectRows(self, selection: list):
        for i in selection: 
            self.tableWidget.selectRow(i)
            self.tableWidgetMou.selectRow(i)
            self.tableWidgetSur.selectRow(i)
            self.tableWidgetSys.selectRow(i)
            self.tableWidgetTime.selectRow(i)

    def throughput_selected(self):
        #check if dataline exists
        if self.project_dict[self.project_name]["ThroughputData"] not in self.mdi.subWindowList() and self.throughput_open1 == False:
            #file that holds throughput file path and selected dataline color; this will be read by dash app
            path = os.path.abspath("GUI/Dash/throughput_info.txt")
            throughput_info_file = open(path, 'w')
            throughput_info_file.write(self.throughput_json+"\n")
            self.throughput.setChecked(True)

            #get rgb values for graph background color
            color = self.color_picker()
            if color is None:
                return 
            else:
                throughput_info_file.write(str(color.getRgb())+"\n")
                throughput_info_file.close()

                self.web = QWebEngineView()
                self.manager_instance.runWebEngine() #start dash
                self.web.load(QUrl("http://127.0.0.1:8050")) #dash app rendered on browser
                self.web.loadStarted.connect(self.loadstarted)
                self.web.loadProgress.connect(self.loadprogress)
                self.web.loadFinished.connect(self.loadfinished)
                throughput_info_file.close()

        elif self.throughput_open1 == True:
            if self.throughput.isChecked() == False:
                self.checkHidden(self.subTh, self.web)
                self.throughput.setChecked(True)
            
            else:
                self.mdi.setActiveSubWindow(self.subTh)
                self.mdi.closeActiveSubWindow()
                self.subTh.hide()
    
    def keypresses_selected(self):
        if self.project_dict[self.project_name]["KeypressData"] not in self.mdi.subWindowList() and self.keypress.isChecked()==True:
            self.keypress.setChecked(True)
            self.subK = QMdiSubWindow()
            self.subK.resize(840,210)
            self.subK.setWindowTitle("Keypresses")
            color = self.color_picker()
            if color is None:
                return 
            else:
                self.subK.setStyleSheet("QTableView { background-color: %s}" % color.name())

                WiresharkColors(self.subK.windowTitle(), color.getRgb())

                self.subK.setWidget(QTextEdit())
                data = self.key_json

                count_row = 0
                self.tableWidget = QTableWidget (self)
                label = "keypresses"
                self.tableWidget = TextDataline(data, label, count_row, 5)
                self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
                self.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
                self.tableWidget.setObjectName("Keypresses")
                self.tableWidget.cellClicked.connect(self.getCoords)
                self.tableWidget.doubleClicked.connect(self.table_clicked)

                self.subK.setWidget(self.tableWidget)
                self.mdi.addSubWindow(self.subK)

                self.tableWidget.show()
                self.subK.show()
                self.project_dict[self.project_name]["KeypressData"] = self.subK
                
                if self.subK.windowStateChanged:
                    self.window_changed("K")

        elif self.keypress.isChecked()==False:
            self.mdi.setActiveSubWindow(self.subK)
            self.mdi.closeActiveSubWindow()
            self.subK.hide()
        else:
            #check if window is hidden
            self.checkHidden(self.subK, self.tableWidget)

    def syscalls_selected(self):
        if self.project_dict[self.project_name]["SystemCallsData"] not in self.mdi.subWindowList() and self.syscalls.isChecked()==True:
            self.syscalls.setChecked(True)
            self.subSC = QMdiSubWindow()
            self.subSC.resize(840,210)
            self.subSC.setWindowTitle("System Calls")

            color = self.color_picker()
            if color is None:
                return 
            else:
                self.subSC.setStyleSheet("QTableView { background-color: %s}" % color.name())

                WiresharkColors(self.subSC.windowTitle(), color.getRgb())

                self.subSC.setWidget(QTextEdit())
                data =  self.sys_json
                count_row = 0

                self.tableWidgetSys = QTableWidget (self)
                label = "systemcalls"
                self.tableWidgetSys = TextDataline(data, label, count_row, 5)
                self.tableWidgetSys.setSelectionBehavior(QAbstractItemView.SelectRows)
                self.tableWidgetSys.setSelectionMode(QAbstractItemView.SingleSelection)
                self.tableWidgetSys.setObjectName("Systemcalls")
                self.tableWidgetSys.cellClicked.connect(self.getCoords)
                self.tableWidgetSys.doubleClicked.connect(self.table_clicked)

                self.subSC.setWidget(self.tableWidgetSys)
                self.mdi.addSubWindow(self.subSC)

                self.tableWidgetSys.show()
                self.subSC.show()
                self.project_dict[self.project_name]["SystemCallsData"] = self.subSC
                
                if self.subSC.windowStateChanged:
                    self.window_changed("Sy")

        elif self.syscalls.isChecked()==False:
            self.mdi.setActiveSubWindow(self.subSC)
            self.mdi.closeActiveSubWindow()
            self.subSC.hide()

        else:
            #check if window is hidden
            self.checkHidden(self.subSC, self.tableWidgetSys)
    
    def suricata_selected(self):
        if self.project_dict[self.project_name]["SuricataData"] not in self.mdi.subWindowList():
            self.subS = QMdiSubWindow()
            self.subS.resize(840,210)
            self.subS.setWindowTitle("Suricata")
            color = self.color_picker()
            if color is None:
                return 
            else:
                self.subS.setStyleSheet("QTableView { background-color: %s}" % color.name())

                self.subS.setWidget(QTextEdit())
                data = self.suricata_json

                count_row = 0
                self.tableWidgetSur = QTableWidget (self)

                label = "suricata"
                self.tableWidgetSur = TextDataline(data, label, count_row, 5)

                self.tableWidgetSur.setSelectionBehavior(QAbstractItemView.SelectRows)
                self.tableWidgetSur.setSelectionMode(QAbstractItemView.SingleSelection)
                self.tableWidgetSur.setObjectName("Suricata Alerts")
                self.tableWidgetSur.cellClicked.connect(self.getCoords)
                self.tableWidgetSur.doubleClicked.connect(self.table_clicked)

                self.subS.setWidget(self.tableWidgetSur)
                self.mdi.addSubWindow(self.subS)

                self.tableWidgetSur.show()
                self.subS.show()
                self.project_dict[self.project_name]["SuricataData"] = self.subS

        else:
            #check if window is hidden
            self.checkHidden(self.subS, self.tableWidgetSur)

    ####SAVE
    def saveDataline(self):

        active = self.mdi.activeSubWindow()
        Projectpath = self.ProjectFolder[0]

        try:
            instanceTableKeyp = self.tableWidget
            save.save(instanceTableKeyp, "keypresses", Projectpath)
        except:
            pass

        try:
            instanceTableSys = self.tableWidgetSys
            save.save(instanceTableSys, "systemcalls", Projectpath)
        except:
            pass

        try:
            instanceTableMou = self.tableWidgetMou
            save.save(instanceTableMou, "mouseclicks", Projectpath)
        except:
            pass

        try:
            instanceTableTimed = self.tableWidgetTime
            save.save(instanceTableTimed, "timed", Projectpath)

        except:
            pass
               
    def trigger_refresh(self):
        try:
            # TRIGGER PACKET COMMENTS PARSER
            if sys.platform == "linux" or sys.platform == "linux2":
                Projectpath = self.ProjectFolder[0]
            else:
                temp = self.ProjectFolder[0].rsplit('\\', 1)
                Projectpath = temp[0]

            commentsParser(Projectpath)

            packetscomments_jsonpath = self.packetsComments_json
            label = "packetcomments"
            count_row = 0
            instance = self.tableWidgetPackets  ##creating instance of table

            reloadDataline.reloadDataline(instance, packetscomments_jsonpath, label)
        except:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Critical)
            msgBox.setText("Error")
            msgBox.setWindowTitle("Error")
            msgBox.setInformativeText("Please open the comments dataline first!")
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec_()

    def watch_PCAP(self):
        self.file_watcher = QFileSystemWatcher()
        if sys.platform == "linux" or sys.platform == "linux2":
            pass
        else:
            temp = self.ProjectFolder[0].rsplit('\\',1)
            self.PCAPpath = temp[0]
            
        self.file_watcher.addPath(self.PCAPpath) #listens for file changes
        self.file_watcher.fileChanged.connect(self.trigger_refresh)
    
    def packetComments_selected(self):
        sub = QMdiSubWindow()
        sub.resize(840,210)
        sub.setWindowTitle("Packets Comments")
        color = self.color_picker()
        sub.setStyleSheet("QTableView { background-color: %s}" % color.name())
        sub.setWidget(QTextEdit())
        data = self.packetsComments_json

        count_row = 0
        self.tableWidgetPackets = QTableWidget (self)

        label = "packetcomments"
        self.tableWidgetPackets = TextDataline(data, label, count_row, 8)

        self.tableWidgetPackets.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidgetPackets.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tableWidgetPackets.setObjectName("Packets Comments")
        self.tableWidgetPackets.cellClicked.connect(self.getCoords)
        self.tableWidgetPackets.doubleClicked.connect(self.table_clicked)
      
        self.watch_PCAP() #WATCH PCAP CHANGE

        sub.setWidget(self.tableWidgetPackets)
        self.mdi.addSubWindow(sub)

        self.tableWidgetPackets.show()
        sub.show()

    def mouse_selected(self):
        if self.project_dict[self.project_name]["MouseClicksData"] not in self.mdi.subWindowList() and self.mouse.isChecked()==True:
            self.mouse.setChecked(True)
            self.subM = QMdiSubWindow()
            self.subM.resize(840,260)
            self.subM.setWindowTitle("Mouse Clicks")
            color = self.color_picker()
            if color is None:
                return 
            else:
                self.subM.setStyleSheet("QTableView { background-color: %s}" % color.name())
                WiresharkColors(self.subM.windowTitle(), color.getRgb())

                self.subM.setWidget(QTextEdit())
                df = self.mouse_json
                count_row = 0

                self.tableWidgetMou = QTableWidget (self)
                self.tableWidgetMou = First(df, self.clicks_path, count_row, 6)
                self.tableWidgetMou.setSelectionBehavior(QAbstractItemView.SelectRows)
                self.tableWidgetMou.setSelectionMode(QAbstractItemView.SingleSelection)
                self.tableWidgetMou.setObjectName("Mouseclicks")
                self.tableWidgetMou.cellClicked.connect(self.getCoords)
                self.tableWidgetMou.doubleClicked.connect(self.table_clicked)

                self.subM.setWidget(self.tableWidgetMou)
                self.mdi.addSubWindow(self.subM)
                self.tableWidgetMou.show()
                self.subM.show()
                self.project_dict[self.project_name]["MouseClicksData"] = self.subM

                if self.subSC.windowStateChanged:
                    self.window_changed("MC")

        elif self.mouse.isChecked()==False:
            self.mdi.setActiveSubWindow(self.subM)
            self.mdi.closeActiveSubWindow()
            self.subM.hide()

        else:
            #check if window is hidden
            self.checkHidden(self.subM, self.tableWidgetMou)

    def timed_selected(self):
        if self.project_dict[self.project_name]["TimedData"] not in self.mdi.subWindowList() and self.timed.isChecked()==True:
            self.timed.setChecked(True)
            self.subT = QMdiSubWindow()
            self.subT.resize(840,260)
            self.subT.setWindowTitle("Timed Screenshots")
            color = self.color_picker()
            if color is None:
                return 
            else:
                self.subT.setStyleSheet("QTableView { background-color: %s}" % color.name())

                WiresharkColors(self.subT.windowTitle(), color.getRgb())

                self.subT.setWidget(QTextEdit())
                df = self.timed_json

                count_row = 0

                self.tableWidgetTime = QTableWidget (self)
                self.tableWidgetTime = Timed(df, self.timed_path, count_row, 6)
                self.tableWidgetTime.setSelectionBehavior(QAbstractItemView.SelectRows)
                self.tableWidgetTime.setSelectionMode(QAbstractItemView.SingleSelection)
                self.tableWidgetTime.setObjectName("TimedScreenshots")
                self.tableWidgetTime.cellClicked.connect(self.getCoords)
                self.tableWidgetTime.doubleClicked.connect(self.table_clicked)

                self.subT.setWidget(self.tableWidgetTime)
                self.mdi.addSubWindow(self.subT)
                self.tableWidgetTime.show()
                self.subT.show()
                self.project_dict[self.project_name]["TimedData"] = self.subT
                
                if self.subSC.windowStateChanged:
                    self.window_changed("Ti")

        elif self.timed.isChecked()==False:
            self.mdi.setActiveSubWindow(self.subT)
            self.mdi.closeActiveSubWindow()
            self.subT.hide()

        else:
            #check if window is hidden
            self.checkHidden(self.subT, self.tableWidgetTime)

    def tile_selected(self):
        self.mdi.tileSubWindows() 

    def choose_json(self):
        f = QFileDialog()
        filenames, _ = QFileDialog.getOpenFileName(f, "Select JSON file")

        if len(filenames) < 0:
            logging.debug("File choose cancelled")
            return

        if len(filenames) > 0:
            json_chosen_path = str(filenames)

            try:
                open_f = open(json_chosen_path, "r")
                open_json = json.load(open_f)
                for j in open_json:
                    mouse_key = "clicks_id"
                    timed_key = "timed_id"
                    keypress_key = "keypresses_id"
                    syscalls_key = "auditd_id"
                    throughput_key = "traffic_xy_id"
                    suricata_key = "suricata_id"
                    packetsComments_key = "packet_id"

                    if mouse_key in j:
                        self.mouse_json = json_chosen_path
                        self.mouse_selected()
                        return
                    elif timed_key in j:
                        self.timed_json = json_chosen_path
                        self.timed_selected()
                        return
                    elif keypress_key in j:
                        self.key_json = json_chosen_path
                        self.keypresses_selected()
                        return
                    elif syscalls_key in j:
                        self.sys_json = json_chosen_path
                        self.syscalls_selected()
                        return
                    elif throughput_key in j:
                        self.throughput_json = json_chosen_path
                        self.throughput_selected()
                        return
                    elif suricata_key in j:
                        self.suricata_json = json_chosen_path
                        self.suricata_selected()
                        return
                    elif packetsComments_key in j:
                        self.packetsComments_json = json_chosen_path
                        self.packetComments_selected()
                        return

                open_f.close()
                
            except IOError:
                print("Cant Open File")

    def color_picker(self):
        color = QColorDialog.getColor()
        if not color.isValid():
            return 
        else:
            return color   

    def contextMenuEvent(self, event):
        menu = QMenu(self)
        addRow = menu.addAction("Add Row")
        delRow = menu.addAction("Delete Row")
        addTag = menu.addAction ("Add Tag")

        action = menu.exec_(event.globalPos())
        if action == addRow:
            self.addRow()
        elif action == delRow:
            self.delRow()
        elif action == addTag:
            self.addTagSignal()

    def addTagSignal(self):
        active = self.mdi.activeSubWindow()

        if active == self.subK:
            table = self.tableWidget
        elif active == self.subSC:
            table = self.tableWidgetSys

        elif active == self.subM:
            table = self.tableWidgetMou
        
        elif active == self.subT:
           table = self.tableWidgetTime
        
        else: 
            return
        
        headercount = table.columnCount()
        row = table.currentItem().row()

        for x in range(0,headercount,1):
            headertext = table.horizontalHeaderItem(x).text()
            if "Tag" == headertext:
                cell_text = table.item(row, x).text()   # get cell at row, col
                self.trigger_tag(cell_text, table, row, x)
            else:
                pass

    def trigger_tag(self, text_to_edit, table, row, x):
        self.tableEdit = table
        self.rowEdit = row
        self.xEdit = x
        self.add_tag = AddTagDialog(text_to_edit)
        self.add_tag.added.connect(self.tag_done)
        self.add_tag.show()

    def addRow(self):
        active = self.mdi.activeSubWindow()
        current = time.time()
        col_timestamp = datetime.datetime.fromtimestamp(current).strftime('%Y-%m-%dT%H:%M:%S')
        cellinfo = QTableWidgetItem(col_timestamp)

        if active == self.subK:
            self.tableWidget.insertRow(self.tableWidget.currentRow())
            columns = self.tableWidget.columnCount()-1
            rows = self.tableWidget.rowCount()-1
            for i in range(columns):
                if i == 0:
                    self.tableWidget.setItem(self.tableWidget.currentRow()-1, i, QTableWidgetItem(str(rows)))
                else:
                    self.tableWidget.setItem(self.tableWidget.currentRow()-1, i, QTableWidgetItem(""))
            self.tableWidget.setItem(self.tableWidget.currentRow()-1, self.tableWidget.columnCount()-1, cellinfo)

        elif active == self.subSC:
            self.tableWidgetSys.insertRow(self.tableWidgetSys.currentRow())
            columns = self.tableWidgetSys.columnCount()-1
            rows = self.tableWidgetSys.rowCount()-1

            it = QtWidgets.QTableWidgetItem()
            tableid = int(rows)
            it.setData(QtCore.Qt.DisplayRole, (tableid))

            for i in range(columns):
                if i == 0:
                    self.tableWidgetSys.setItem(self.tableWidgetSys.currentRow()-1, i, it)
                else:
                    self.tableWidgetSys.setItem(self.tableWidgetSys.currentRow()-1, i, QTableWidgetItem(""))
            self.tableWidgetSys.setItem(self.tableWidgetSys.currentRow()-1, self.tableWidgetSys.columnCount()-1, cellinfo)

        elif active == self.subM:
            self.tableWidgetMou.insertRow(self.tableWidgetMou.currentRow())
            columns = self.tableWidgetMou.columnCount()-1
            rows = self.tableWidgetMou.rowCount()-1
            for i in range(columns):
                if i == 0:
                    self.tableWidgetMou.setItem(self.tableWidgetMou.currentRow()-1, i, QTableWidgetItem(str(rows)))
                else:
                    self.tableWidgetMou.setItem(self.tableWidgetMou.currentRow()-1, i, QTableWidgetItem(""))
            self.tableWidgetMou.setItem(self.tableWidgetMou.currentRow()-1, self.tableWidgetMou.columnCount()-1, cellinfo)
        
        elif active == self.subT:
            self.tableWidgetTime.insertRow(self.tableWidgetTime.currentRow())
            columns = self.tableWidgetTime.columnCount()-1
            rows = self.tableWidgetTime.rowCount()-1
            for i in range(columns):
                if i == 0:
                    self.tableWidgetTime.setItem(self.tableWidgetTime.currentRow()-1, i, QTableWidgetItem(str(rows)))
                else:
                    self.tableWidgetTime.setItem(self.tableWidgetTime.currentRow()-1, i, QTableWidgetItem(""))
            self.tableWidgetTime.setItem(self.tableWidgetTime.currentRow()-1, self.tableWidgetTime.columnCount()-1, cellinfo)
    
        elif active == self.subS:
            self.tableWidgetSur.insertRow(self.tableWidgetSur.currentRow())
            columns = self.tableWidgetSur.columnCount()-1
            rows = self.tableWidgetSur.rowCount()-1
            for i in range(columns):
                if i == 0:
                    self.tableWidgetSur.setItem(self.tableWidgetSur.currentRow()-1, i, QTableWidgetItem(str(rows)))
                else:
                    self.tableWidgetSur.setItem(self.tableWidgetSur.currentRow()-1, i, QTableWidgetItem(""))
            self.tableWidgetSur.setItem(self.tableWidgetSur.currentRow()-1, self.tableWidgetSur.columnCount()-1, cellinfo)
        
        else: 
            return
    
    def delRow(self):
        active = self.mdi.activeSubWindow()
        if active == self.subK:
            if self.tableWidget.rowCount() > 0:
                self.tableWidget.removeRow(self.tableWidget.currentRow())
            else:
                self.delete_pop_up()
        elif active == self.subSC:
            if self.tableWidgetSys.rowCount() > 0:
                self.tableWidgetSys.removeRow(self.tableWidgetSys.currentRow())
            else:
                self.delete_pop_up()
        elif active == self.subM:
            if self.tableWidgetMou.rowCount() > 0:
                self.tableWidgetMou.removeRow(self.tableWidgetMou.currentRow())
            else:
                self.delete_pop_up()
        elif active == self.subT:
            if self.tableWidgetTime.rowCount() > 0:
                self.tableWidgetTime.removeRow(self.tableWidgetTime.currentRow())
            else:
                self.delete_pop_up()
        elif active == self.subS:
            if self.tableWidgetSur.rowCount() > 0:
                self.tableWidgetSur.removeRow(self.tableWidgetSur.currentRow())
            else:
                self.delete_pop_up()

    def delete_pop_up(self):
        QMessageBox.warning(self,
                                "Nothing to delete",
                                "There's nothing to delete",
                                QMessageBox.Ok)            
        return None

    def load_throughput_complete(self):
        self.subTh = QMdiSubWindow()
        self.subTh.resize(840,330)
        self.subTh.setWindowTitle("Throughput")
        loading_label = QLabel("Loading...")
        self.subTh.setWidget(loading_label)
        self.mdi.addSubWindow(self.subTh)
        self.subTh.show()
        self.web.show()
        self.subTh.setWidget(self.web) 
        self.project_dict[self.project_name]["ThroughputData"] = self.subTh
        self.throughput_open1 = True
        if self.subTh.windowStateChanged:
            self.window_changed("Th")

    def export_project(self):
        ExportDialog(self, self.project_path).exec()

    def checkHidden(self, subW, content):
        if subW.isHidden():
            content.show()
            subW.show()
        else:
            return

    def new_import_project(self):
        #reset cancel check, each time this function is called
        self.new_import.emit(True)
    
    def open_prev_project(self):
        #self.open_prev.emit(True)
        return
    
    def window_changed(self, dataline):
        if dataline == "K":
            if self.subK.isHidden() == True:
                self.keypress.setChecked(False)
            else:
                self.keypress.setChecked(True)
        elif dataline == "Sy":
            if self.subSC.isHidden() == True:
                self.syscalls.setChecked(False)
            else:
                self.syscalls.setChecked(True)
        elif dataline == "MC":
            if self.subM.isHidden() == True:
                self.mouse.setChecked(False)
            else:
                self.mouse.setChecked(True)
        elif dataline == "Ti":
            if self.subT.isHidden() == True:
                self.timed.setChecked(False)
            else:
                self.timed.setChecked(True)
        elif dataline == "Th":
            if self.subTh.isHidden() == True:
                self.throughput.setChecked(False)
            else:
                self.throughput.setChecked(True)

    def trigger_edit(self, text_to_edit, table, row, x):
        self.tableEdit = table
        self.rowEdit = row
        self.xEdit = x
        self.edit_text = EditTextDialog(text_to_edit)
        self.edit_text.edited.connect(self.edit_done)
        self.edit_text.show()

    @QtCore.pyqtSlot(str)
    def edit_done(self, edited_text):
        self.tableEdit.setItem(self.rowEdit, self.xEdit, QTableWidgetItem(edited_text))

    @QtCore.pyqtSlot(str)
    def tag_done(self, edited_text):
        self.tableEdit.setItem(self.rowEdit, self.xEdit, QTableWidgetItem(edited_text))

    @QtCore.pyqtSlot(int)
    def loadprogress(self, progress):
        self.progress.show()
        count = 0
        while(count < 100):
            count += 1
            time.sleep(0.02)
            self.progress.setBarValue(count)
    
    @QtCore.pyqtSlot()
    def loadstarted(self):
        print(time.time(), ": load started")
    
    @QtCore.pyqtSlot()
    def loadfinished(self):
        self.progress.hide()
        print(time.time(), ": load finished")
        if self.throughput_open1 == False:
            #load the dataline
            self.load_throughput_complete()
        else:
            self.subTh.showMaximized()
            self.subTh.showNormal()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Close Timeline View', 'Are you sure you want to exit?', 
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            reply2 = QMessageBox.question(self, 'Close Timeline View', 'Do you want to save your progress?', 
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

            if reply == QMessageBox.Yes:
                self.saveDataline()

            elif reply == QMessageBox.No and not type(event) == bool:
                event.ignore()

            if(self.web != ''):
                self.web.close()
                self.manager_instance.stopWebEngine()
            
            self.manager_instance.stopWireshark()
            clearFilters()
            qApp.quit()
            return
            
        elif reply == QMessageBox.No and not type(event) == bool:
            event.ignore()
        
        else:
            pass
        return