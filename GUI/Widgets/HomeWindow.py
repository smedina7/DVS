import logging
import os
import time
from re import search
import subprocess
import json

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWebEngineWidgets import *
from GUI.Widgets.AbstractTable import pandasModel
from GUI.Widgets.textdataline import TextDataline
from GUI.Widgets.Mouseclicks import First
from GUI.Widgets.TimedScreenshots import Timed
import pandas as pd
from GUI.Widgets.Timestamp import Timestamp
from GUI.PacketView.WiresharkColorFilters import WiresharkColors, clearFilters
from GUI.Threading.BatchThread import BatchThread
from GUI.Dialogs.ProgressBarDialog import ProgressBarDialog
from GUI.Dialogs.ExportDialog import ExportDialog

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

        self.key_json = ''
        self.sys_json = ''
        self.mouse_json = ''
        self.timed_json = ''
        self.suricata_json = ''
        self.throughput_json = throughput_path + '/parsed/tshark/networkDataXY.JSON'

        self.project_name = os.path.basename(self.project_path)

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

    def file_changed(self):
        self.syncWindows(1)

    def buttonaction_wireshark(self, b):
        if b == True:
            self.sync_button_wireshark.setText("Wireshark Sync : on")
            self.wiresharkTrigger = True
        else:
            self.sync_button_wireshark.setText("Wireshark Sync : off")
            self.wiresharkTrigger = False

    def syncWindows(self, b):
        if self.timestampTrigger:
            children = self.findChildren(QTableWidget)
            for child in children:
                child.setSelectionMode(QAbstractItemView.MultiSelection)
                columncount = child.columnCount()
                child.clearSelection()
                for row in range(child.rowCount()):
                    indexTimeStamp = child.item(row,columncount-1).text()
                    if b == -1:
                        if self.timestamp == indexTimeStamp:
                            child.selectRow(row)
                            Timestamp.update_timestamp(self.timestamp)#writes to timestamp.txt
                    else:
                        currTimeStamp = Timestamp.get_current_timestamp()#reads timestamp.txt
                        if indexTimeStamp == currTimeStamp:
                            #child.clearSelection()
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
            self.file_watcher = QFileSystemWatcher()
            self.file_watcher.addPath('/home/kali/DVS/GUI/Dash/timestamp.txt') #listens for file changes
            self.file_watcher.fileChanged.connect(self.file_changed)
            # redraw
            self.syncWindows(-1)
        else:
            self.sync_button_timestamp.setText("Timestamp Sync : off")
            self.timestampTrigger = False
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
            print("First IF")
            #file that holds throughput file path and selected dataline color; this will be read by dash app
            path = os.path.abspath("GUI/Dash/throughput_info.txt")
            throughput_info_file = open(path, 'w')
            throughput_info_file.write(self.throughput_json+"\n")

            #get rgb values for graph background color
            color = self.color_picker()
            if color is None:
                print("no color selected")
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

        elif self.throughput_open1 == True:
            print("Second IF")
            self.checkHidden(self.subTh, self.web)
            
        else:
            print("Third IF")
            #check if window is hidden
            self.checkHidden(self.subTh, self.web)
    
    def keypresses_selected(self):
        if self.project_dict[self.project_name]["KeypressData"] not in self.mdi.subWindowList() and self.keypress.isChecked()==True:
            self.subK = QMdiSubWindow()
            self.subK.resize(840,210)
            self.subK.setWindowTitle("Keypresses")
            color = self.color_picker()
            if color is None:
                print("no color selected")
                return 
            else:
                self.subK.setStyleSheet("QTableView { background-color: %s}" % color.name())

                WiresharkColors(self.subK.windowTitle(), color.getRgb())

                self.subK.setWidget(QTextEdit())
                data = self.key_json

                count_row = 0
                self.tableWidget = QTableWidget (self)
                label = "keypresses"
                self.tableWidget = TextDataline(data, label, count_row, 4)
                self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
                self.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
                self.tableWidget.setObjectName("Keypresses")
                self.tableWidget.cellClicked.connect(self.getCoords)
                
                self.subK.setWidget(self.tableWidget)
                self.mdi.addSubWindow(self.subK)

                self.tableWidget.show()
                self.subK.show()
                self.project_dict[self.project_name]["KeypressData"] = self.subK
        elif self.keypress.isChecked()==False:
            self.mdi.setActiveSubWindow(self.subK)
            self.mdi.closeActiveSubWindow()
            self.subK.hide()
        else:
            #check if window is hidden
            self.checkHidden(self.subK, self.tableWidget)

    def syscalls_selected(self):
        if self.project_dict[self.project_name]["SystemCallsData"] not in self.mdi.subWindowList() and self.syscalls.isChecked()==True:
            self.subSC = QMdiSubWindow()
            self.subSC.resize(840,210)
            self.subSC.setWindowTitle("System Calls")

            color = self.color_picker()
            if color is None:
                print("no color selected")
                return 
            else:
                self.subSC.setStyleSheet("QTableView { background-color: %s}" % color.name())

                WiresharkColors(self.subSC.windowTitle(), color.getRgb())

                self.subSC.setWidget(QTextEdit())
                data =  self.sys_json
                count_row = 0

                self.tableWidgetSys = QTableWidget (self)
                label = "systemcalls"
                self.tableWidgetSys = TextDataline(data, label, count_row, 4)
                self.tableWidgetSys.setSelectionBehavior(QAbstractItemView.SelectRows)
                self.tableWidgetSys.setSelectionMode(QAbstractItemView.SingleSelection)
                self.tableWidgetSys.setObjectName("Systemcalls")
                self.tableWidgetSys.cellClicked.connect(self.getCoords)

                self.subSC.setWidget(self.tableWidgetSys)
                self.mdi.addSubWindow(self.subSC)

                self.tableWidgetSys.show()
                self.subSC.show()
                self.project_dict[self.project_name]["SystemCallsData"] = self.subSC
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
                print("no color selected")
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

                self.subS.setWidget(self.tableWidgetSur)
                self.mdi.addSubWindow(self.subS)

                self.tableWidgetSur.show()
                self.subS.show()
                self.project_dict[self.project_name]["SuricataData"] = self.subS

        else:
            #check if window is hidden
            self.checkHidden(self.subS, self.tableWidgetSur)

    def mouse_selected(self):
        if self.project_dict[self.project_name]["MouseClicksData"] not in self.mdi.subWindowList() and self.mouse.isChecked()==True:
            self.subM = QMdiSubWindow()
            self.subM.resize(840,260)
            self.subM.setWindowTitle("Mouse Clicks")
            color = self.color_picker()
            if color is None:
                print("no color selected")
                return 
            else:
                self.subM.setStyleSheet("QTableView { background-color: %s}" % color.name())
                WiresharkColors(self.subM.windowTitle(), color.getRgb())

                self.subM.setWidget(QTextEdit())
                df = self.mouse_json
                count_row = 0

                self.tableWidgetMou = QTableWidget (self)
                self.tableWidgetMou = First(df, self.clicks_path, count_row, 5)
                self.tableWidgetMou.setSelectionBehavior(QAbstractItemView.SelectRows)
                self.tableWidgetMou.setSelectionMode(QAbstractItemView.SingleSelection)
                self.tableWidgetMou.setObjectName("Mouseclicks")
                self.tableWidgetMou.cellClicked.connect(self.getCoords)

                self.subM.setWidget(self.tableWidgetMou)
                self.mdi.addSubWindow(self.subM)
                self.tableWidgetMou.show()
                self.subM.show()
                self.project_dict[self.project_name]["MouseClicksData"] = self.subM
        elif self.mouse.isChecked()==False:
            self.mdi.setActiveSubWindow(self.subM)
            self.mdi.closeActiveSubWindow()
            self.subM.hide()

        else:
            #check if window is hidden
            self.checkHidden(self.subM, self.tableWidgetMou)

    def timed_selected(self):
        if self.project_dict[self.project_name]["TimedData"] not in self.mdi.subWindowList() and self.timed.isChecked()==True:
            self.subT = QMdiSubWindow()
            self.subT.resize(840,260)
            self.subT.setWindowTitle("Timed Screenshots")
            color = self.color_picker()
            if color is None:
                print("no color selected")
                return 
            else:
                self.subT.setStyleSheet("QTableView { background-color: %s}" % color.name())

                WiresharkColors(self.subT.windowTitle(), color.getRgb())

                self.subT.setWidget(QTextEdit())
                df = self.timed_json

                count_row = 0

                self.tableWidgetTime = QTableWidget (self)
                self.tableWidgetTime = Timed(df, self.timed_path, count_row, 5)
                self.tableWidgetTime.setSelectionBehavior(QAbstractItemView.SelectRows)
                self.tableWidgetTime.setSelectionMode(QAbstractItemView.SingleSelection)
                self.tableWidgetTime.setObjectName("TimedScreenshots")
                self.tableWidgetTime.cellClicked.connect(self.getCoords)

                self.subT.setWidget(self.tableWidgetTime)
                self.mdi.addSubWindow(self.subT)
                self.tableWidgetTime.show()
                self.subT.show()
                self.project_dict[self.project_name]["TimedData"] = self.subT

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
        menu = QMenu(self.tableWidget)
        addRow = menu.addAction("Add Row")
        addColumn = menu.addAction("Add Column")
        delColumn = menu.addAction("Delete Column")
        delRow = menu.addAction("Delete Row")
        duplicateRow = menu.addAction("Duplicate Row")
        duplicateColumn = menu.addAction("Duplicate Column")

        action = menu.exec_(event.globalPos())
        if action == addRow:
            self.addRow()
        elif action ==addColumn:
            self.addColumn()
        elif action == delColumn:
            self.delColumn()
        elif action == delRow:
            self.delRow()
        elif action == duplicateRow:
            self.duplicateRow()
        elif action == duplicateColumn:
            self.duplicateColumn()

    def addRow(self):
        rowCount = self.tableWidget.rowCount()
        self.tableWidget.insertRow(rowCount)
        print("New Row Added")

    def addColumn(self):
        colCount = self.tableWidget.columnCount()
        self.tableWidget.insertColumn(colCount)
        print("New Column Added")
    
    def delRow(self):
        if self.tableWidget.rowCount()>0:
            self.tableWidget.removeRow(self.tableWidget.rowCount() -1)
            print("Row deleted")
    
    def delColumn(self):
        if self.tableWidget.columnCount()>0:
            self.tableWidget.removeColumn(self.tableWidget.columnCount() -1)
            print("Column deleted")

    def duplicateRow(self):
        self.tableWidget.insertRow(self.tableWidget.rowCount())
        rowCount = self.tableWidget.rowCount()
        columnCount = self.tableWidget.columnCount()

        for j in range(columnCount):
            if not self.tableWidget.item(rowCount-2, j) is None:
                self.tableWidget.setItem(rowCount-1, j, QTableWidgetItem(self.tableWidget.item(rowCount-2, j).text()))
        print("Row Duplicated")

    def duplicateColumn(self):
        self.tableWidget.insertColumn(self.tableWidget.columnCount())
        columnCount = self.tableWidget.columnCount()
        rowCount = self.tableWidget.rowCount()

        for j in range(rowCount):
            if not self.tableWidget.item(j, columnCount-2) is None:
                self.tableWidget.setItem(j, columnCount-1, QTableWidgetItem(self.tableWidget.item(j, columnCount-2).text()))
        print("Column Duplicated")
    
    def load_throughput_complete(self):
        self.subTh = QMdiSubWindow()
        self.subTh.resize(840,320)
        self.subTh.setWindowTitle("Throughput")
        loading_label = QLabel("Loading...")
        self.subTh.setWidget(loading_label)
        self.mdi.addSubWindow(self.subTh)
        self.subTh.show()
        self.web.show()
        self.subTh.setWidget(self.web) 
        self.project_dict[self.project_name]["ThroughputData"] = self.subTh
        self.throughput_open1 = True
        print(self.throughput_open1)

    def export_project(self):
        ExportDialog(self, self.project_path).exec()

    def checkHidden(self, subW, content):
        if subW.isHidden():
            content.show()
            subW.show()
        else:
            print("Dataline already open")

    def new_import_project(self):
        #reset cancel check, each time this function is called
        self.new_import.emit(True)
    
    def open_prev_project(self):
        #self.open_prev.emit(True)
        print("open prev triggered")

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

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Close Timeline View', 'Are you sure you want to exit?', 
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
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