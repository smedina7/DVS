import logging
import os
import time
from re import search
import subprocess

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWebEngineWidgets import *
from GUI.Widgets.AbstractTable import pandasModel
from GUI.Widgets.textdataline import Keypresses, SystemCalls
from GUI.Widgets.Mouseclicks import First
from GUI.Widgets.TimedScreenshots import Timed
import pandas as pd

from GUI.Threading.BatchThread import BatchThread
from GUI.Dialogs.ProgressBarDialog import ProgressBarDialog

class MainGUI(QMainWindow):
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

        self.key_json = ''
        self.sys_json = ''
        self.mouse_json = ''
        self.timed_json = ''
        self.throughput_json = throughput_path + '/parsed/tshark/networkDataXY.JSON'

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
        self.tb.addWidget(self.sync_button_wireshark)
        self.sync_button_wireshark.clicked.connect(self.buttonaction_wireshark)

        # Timestamp sync button
        self.sync_button_timestamp = QPushButton(self.tb)
        self.sync_button_timestamp.setCheckable(True)
        self.sync_button_timestamp.setText("Timestamp Sync: off")
        self.tb.addWidget(self.sync_button_timestamp)
        self.sync_button_timestamp.clicked.connect(self.buttonaction_timestamp)

        #Set area for where datalines are going to show
        self.mdi = QMdiArea()
        self.setCentralWidget(self.mdi)

        #add scrollbar
        self.mdi.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.mdi.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        #Add menu bar
        bar = self.menuBar()
        file = bar.addMenu("File")

        #add default datalines
        add_dataline = bar.addMenu("Add Dataline")
        preset_dataline = add_dataline.addMenu("Preset Dataline")
        custom_dataline = add_dataline.addAction("Choose JSON")

        throughput = preset_dataline.addAction("Throughput")
        keypress = preset_dataline.addAction("Keypresses")
        syscalls = preset_dataline.addAction("System Calls")
        mouse = preset_dataline.addAction("Mouse Clicks")
        timed = preset_dataline.addAction("Timed Screenshots")
        
        #dataline windows actions
        throughput.triggered.connect(self.throughput_selected)
        self.resizeEvent(throughput.triggered)
        keypress.triggered.connect(self.keypresses_selected)
        self.resizeEvent(keypress.triggered)
        syscalls.triggered.connect(self.syscalls_selected)
        self.resizeEvent(syscalls.triggered)
        mouse.triggered.connect(self.mouse_selected)
        self.resizeEvent(mouse.triggered)
        timed.triggered.connect(self.timed_selected)
        self.resizeEvent(timed.triggered)

        custom_dataline.triggered.connect(self.choose_json)
        self.resizeEvent(custom_dataline.triggered)

        adjust = bar.addMenu("Adjust Subwindows")
        adjust.addAction("Tile Layout")
        adjust.triggered[QAction].connect(self.tile_selected)

        #Home Window Widget Configuration
        self.setWindowTitle("Timeline View")
        self.setMinimumHeight(700)
        self.setMinimumWidth(800)
        # sync stuff
        self.timestamp = ""
        self.timestampTrigger = False

    def buttonaction_wireshark(self, b):
        if b == True:
            self.sync_button_wireshark.setText("Wireshark Sync : on")
            self.wiresharkTrigger = True
        else:
            self.sync_button_wireshark.setText("Wireshark Sync : off")
            self.wiresharkTrigger = False

    def syncWindows(self):
        if self.timestampTrigger:
            children = self.findChildren(QTableWidget)
            for child in children:
                child.setSelectionMode(QAbstractItemView.MultiSelection)
                columncount = child.columnCount()
                child.clearSelection()
                for row in range(child.rowCount()):
                    indexTimeStamp = child.item(row,columncount-1).text()
                    if self.timestamp == indexTimeStamp:
                        child.selectRow(row)
                    #child.show()
        if self.timestampTrigger == False:
            children = self.findChildren(QTableWidget)
            for child in children:
                child.setSelectionMode(QAbstractItemView.SingleSelection)
                child.clearSelection()
                #child.show()

    def buttonaction_timestamp(self, b):
        if b == True:
            self.sync_button_timestamp.setText("Timestamp Sync : on")
            self.timestampTrigger = True
            # redraw
            self.syncWindows()
        else:
            self.sync_button_timestamp.setText("Timestamp Sync : off")
            self.timestampTrigger = False
            # undraw
            self.timestamp = ""
            self.syncWindows()

    def resizeEvent(self, event):
        self.sizeHint()

    def getCoords(self, r , c):
        sender = self.sender()
        name = sender.objectName()
        table = self.findChild(QTableWidget, name)
        columncount = table.columnCount()
        indexTimeStamp = table.item(r,columncount-1).text()
        if (self.timestampTrigger):
            # stamp = DateFormat("yyyy-MM-dd'T'HH:MM:ss")
            self.timestamp = indexTimeStamp
            self.syncWindows()

    def selectRows(self, selection: list):
        for i in selection: 
            self.tableWidget.selectRow(i)

    def throughput_selected(self):
        #file that holds throughput file path and selected dataline color; this will be read by dash app
        path = os.path.abspath("GUI/Dash/throughput_info.txt")
        throughput_info_file = open(path, 'w')
        throughput_info_file.write(self.throughput_json+"\n")

        #get rgb values for graph background color
        color = self.color_picker()
        throughput_info_file.write(str(color.getRgb())+"\n")
        throughput_info_file.close()

        self.web = QWebEngineView()
        self.manager_instance.runWebEngine() #start dash
        self.web.load(QUrl("http://127.0.0.1:8050")) #dash app rendered on browser
        self.web.loadStarted.connect(self.loadstarted)
        self.web.loadProgress.connect(self.loadprogress)
        self.web.loadFinished.connect(self.loadfinished)
    
    def keypresses_selected(self):
        sub = QMdiSubWindow()
        sub.resize(700,150)
        sub.setWindowTitle("Keypresses")
        color = self.color_picker()
        sub.setStyleSheet("QTableView { background-color: %s}" % color.name())

        sub.setWidget(QTextEdit())
        data = self.key_json

        count_row = 0
        self.tableWidget = QTableWidget (self)
        self.tableWidget = Keypresses(data, count_row, 4)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tableWidget.setObjectName("Keypresses")
        self.tableWidget.cellClicked.connect(self.getCoords)
        
        sub.setWidget(self.tableWidget)
        self.mdi.addSubWindow(sub)

        self.tableWidget.show()
        sub.show()

    def syscalls_selected(self):
        sub = QMdiSubWindow()
        sub.resize(700,200)
        sub.setWindowTitle("System Calls")

        color = self.color_picker()
        sub.setStyleSheet("QTableView { background-color: %s}" % color.name())

        sub.setWidget(QTextEdit())
        data =  self.sys_json
        count_row = 0

        self.tableWidget = QTableWidget (self)
        self.tableWidget = SystemCalls(data, count_row, 4)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tableWidget.setObjectName("Systemcalls")
        self.tableWidget.cellClicked.connect(self.getCoords)

        sub.setWidget(self.tableWidget)
        self.mdi.addSubWindow(sub)

        self.tableWidget.show()
        sub.show()

    def mouse_selected(self):
        sub = QMdiSubWindow()
        sub.resize(700,150)
        sub.setWindowTitle("Mouse Clicks")
        color = self.color_picker()
        sub.setStyleSheet("QTableView { background-color: %s}" % color.name())

        sub.setWidget(QTextEdit())
        df = self.mouse_json
        count_row = 0

        self.tableWidget = QTableWidget (self)
        self.tableWidget = First(df, self.clicks_path, count_row, 5)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tableWidget.setObjectName("Mouseclicks")
        self.tableWidget.cellClicked.connect(self.getCoords)

        sub.setWidget(self.tableWidget)
        self.mdi.addSubWindow(sub)
        self.tableWidget.show()
        sub.show()

    def timed_selected(self):
        sub = QMdiSubWindow()
        sub.resize(700,150)
        sub.setWindowTitle("Timed Screenshots")
        color = self.color_picker()
        sub.setStyleSheet("QTableView { background-color: %s}" % color.name())

        sub.setWidget(QTextEdit())
        df = self.timed_json

        count_row = 0

        self.tableWidget = QTableWidget (self)
        self.tableWidget = Timed(df, self.timed_path, count_row, 5)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tableWidget.setObjectName("TimedScreenshots")
        self.tableWidget.cellClicked.connect(self.getCoords)

        sub.setWidget(self.tableWidget)
        self.mdi.addSubWindow(sub)
        self.tableWidget.show()
        sub.show()

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

                open_f.close()
                
            except IOError:
                print("Cant Open File")


    def color_picker(self):
        color = QColorDialog.getColor()
        if color == '':
            return 
        else:
            return color      

    def load_throughput_complete(self):
        sub = QMdiSubWindow()
        sub.resize(790,320)
        sub.setWindowTitle("Throughput")
        loading_label = QLabel("Loading...")
        sub.setWidget(loading_label)
        self.mdi.addSubWindow(sub)
        sub.show()
        self.web.show()
        sub.setWidget(self.web)     
    
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
        #load the dataline
        self.load_throughput_complete()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Close Timeline View', 'Are you sure you want to exit?', 
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
            if(self.web != ''):
                self.web.close()
                self.manager_instance.stopWebEngine()
            
            self.manager_instance.stopWireshark()
            
        else:
            event.ignore()