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
from GUI.Widgets.AbstractTable2 import pandasModel2
from GUI.Widgets.AbstractTable2 import pandasModel3
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

        #create color button
        """ self.color_button = QPushButton(self.tb)
        self.color_button.setText("Color")
        self.tb.addWidget(self.color_button)
        self.color_button.clicked.connect(self.color_picker) """

        #Set area for where datalines are going to show
        self.mdi = QMdiArea()
        self.setCentralWidget(self.mdi)

        #add scrollbar
        self.mdi.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.mdi.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        #Add menu bar
        bar = self.menuBar()
        file = bar.addMenu("File")
        file.triggered[QAction].connect(self.windowaction)

        #add default datalines
        add_dataline = bar.addMenu("Add Dataline")
        add_dataline.addAction("Throughput")
        add_dataline.addAction("Keypresses")
        add_dataline.addAction("System Calls")
        add_dataline.addAction("Mouse Clicks")
        add_dataline.addAction("Timed Screenshots")
        
        #dataline windows actions
        add_dataline.triggered[QAction].connect(self.windowaction)
        self.resizeEvent(add_dataline.triggered[QAction])
        adjust = bar.addMenu("Adjust Subwindows")
        adjust.addAction("Tile Layout")
        adjust.triggered[QAction].connect(self.windowaction)

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
            children = self.findChildren(QTableView)
            for child in children:
                child.setSelectionMode(QAbstractItemView.MultiSelection)
                columncount = child.model().columnCount()
                child.clearSelection()
                for row in range(child.model().rowCount()):
                    index = child.model().index(row, columncount - 1)
                    indexTimeStamp = str(child.model().itemData(index))
                    temp = indexTimeStamp[5:len(indexTimeStamp) - 2]
                    if self.timestamp == temp:
                        child.selectRow(row)
                    child.show()
        if self.timestampTrigger == False:
            children = self.findChildren(QTableView)
            for child in children:
                child.setSelectionMode(QAbstractItemView.SingleSelection)
                child.clearSelection()
                child.show()

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

    def getCoords(self, item):
        columncount = item.model().columnCount()
        row = item.row()
        index = item.model().index(row, columncount - 1)
        indexTimeStamp = str(item.model().itemData(index))
        if (self.timestampTrigger):
            # stamp = DateFormat("yyyy-MM-dd'T'HH:MM:ss")
            stamp = indexTimeStamp[5:len(indexTimeStamp) - 2]
            self.timestamp = stamp
            self.syncWindows()

    def windowaction(self, q):
        if q.text() == "Throughput":
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
            
        if q.text() == "Keypresses":
            sub = QMdiSubWindow()
            sub.resize(790,200)
            sub.setWindowTitle("Keypresses")

            #this gives the hex value of the color; can be changed to rgb with 'color.getRgb()' instead of color.name()
            color = self.color_picker()
            sub.setStyleSheet("QTableView { background-color: %s}" % color.name())

            df = pd.read_json (self.key_json)

            model = pandasModel(df)
            view = QTableView()
            view.setModel(model)

            sub.setWidget(view)

            header = view.horizontalHeader()
            view.setColumnWidth(1, 210)
            header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
            self.mdi.addSubWindow(sub)

            view.setSelectionMode(QAbstractItemView.SingleSelection)
            view.clicked.connect(self.getCoords)

            view.show()
            sub.show()

        if q.text() == "System Calls":
            sub = QMdiSubWindow()
            sub.resize(790,200)
            sub.setWindowTitle("System Calls")
            
            #this gives the hex value of the color; can be changed to rgb with 'color.getRgb()' instead of color.name()
            color = self.color_picker()
            sub.setStyleSheet("QTableView { background-color: %s}" % color.name())
            
            df = pd.read_json(self.sys_json)

            model = pandasModel(df)
            view = QTableView()
            view.setModel(model)

            sub.setWidget(view)

            header = view.horizontalHeader()
            view.setColumnWidth(1, 210)
            header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
            self.mdi.addSubWindow(sub)

            view.setSelectionMode(QAbstractItemView.SingleSelection)
            view.clicked.connect(self.getCoords)

            view.show()
            sub.show()

        if q.text() == "Mouse Clicks":
            sub = QMdiSubWindow()
            sub.resize(790,220)
            sub.setWindowTitle("Mouse Clicks")
            
            #this gives the hex value of the color; can be changed to rgb with 'color.getRgb()' instead of color.name()
            color = self.color_picker()
            sub.setStyleSheet("QTableView { background-color: %s}" % color.name())
            
            df = pd.read_json(self.mouse_json)

            model = pandasModel2(df, self.clicks_path)
            view = QTableView()
            view.setModel(model)

            sub.setWidget(view)

            header = view.horizontalHeader()
            view.setColumnWidth(1, 210)
            view.setColumnWidth(2, 50)
            view.setIconSize(QSize(256, 256))
            count_row = df.shape[0]
            for x in range(count_row):
                view.setRowHeight(x,100)
            header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
            self.mdi.addSubWindow(sub)

            view.setSelectionMode(QAbstractItemView.SingleSelection)
            view.clicked.connect(self.getCoords)

            view.show()
            sub.show()

        if q.text() == "Timed Screenshots":
            sub = QMdiSubWindow()
            sub.resize(790,220)
            sub.setWindowTitle("Timed Screenshots")
            
            #this gives the hex value of the color; can be changed to rgb with 'color.getRgb()' instead of color.name()
            color = self.color_picker()
            sub.setStyleSheet("QTableView { background-color: %s}" % color.name())

            df = pd.read_json(self.timed_json)

            model = pandasModel3(df, self.timed_path)
            view = QTableView()
            view.setModel(model)

            sub.setWidget(view)

            header = view.horizontalHeader()
            view.setColumnWidth(4, 210)
            view.setColumnWidth(2, 50) 
            view.setIconSize(QSize(256, 256))
            count_row = df.shape[0]
            for x in range(count_row):
                view.setRowHeight(x,100)

            header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
            self.mdi.addSubWindow(sub)

            view.setSelectionMode(QAbstractItemView.SingleSelection)
            view.clicked.connect(self.getCoords)

            view.show()
            sub.show()

        if q.text() =="Tile Layout":
            self.mdi.tileSubWindows()    

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

            