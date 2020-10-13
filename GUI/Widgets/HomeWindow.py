import logging
import os
import subprocess
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from PyQt5.QtWebEngineWidgets import *
from Widgets.WebEngineView import WebEngine
from Widgets.AbstractTable import pandasModel

import pandas as pd

class MainGUI(QMainWindow):
    def __init__(self, json_files, throughput_path, parent = None):
        logging.debug("MainGUI(): Instantiated")
        super(MainGUI, self).__init__(parent)
        json_file_list = json_files
        throughput_files = throughput_path

        self.key_json = ''
        self.sys_json = ''
        self.mouse_json = ''
        self.throughput_json = ''
        #need self.net_json for reading throughput file

        #Get JSON Files
        #print(json_file_list)
        
        #get path for each file
        for file in json_file_list:
            print(file)

            if "Keypresses.JSON" in file:
                self.key_json = file
            
            if "SystemCalls.JSON" in file:
                self.sys_json = file
            
            if "MouseClicks.JSON" in file:
                self.mouse_json = file

        #for throughput
        throughput_files = os.path.join(throughput_files, "parsed/tshark")
        self.throughput_json = os.path.join(throughput_files, "networkDataXY.JSON")

        #need throughput file
        print(self.key_json)
        print(self.sys_json)
        print(self.mouse_json)
        print(self.throughput_json)


        #Home Window Widget Configuration
        self.setFixedSize(710,565)
        self.setWindowTitle("Timeline View")

        #Create toolbar and sync button widgets
        self.tb = self.addToolBar("")
        self.sync_button = QPushButton(self.tb)
        self.sync_button.setCheckable(True)
        self.sync_button.setText("Unsyncronized")
        self.tb.addWidget(self.sync_button)
        self.sync_button.clicked.connect(self.buttonaction)

        #Set area for where datalines are going to show
        self.mdi = QMdiArea()
        self.setCentralWidget(self.mdi)

        #add scrollbar
        self.mdi.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        #Add menu bar
        bar = self.menuBar()
        file = bar.addMenu("File")
        #file.addAction("Save")
        file.triggered[QAction].connect(self.windowaction)

        #add default datalines
        add_dataline = bar.addMenu("Add Dataline")
        add_dataline.addAction("New Window")
        add_dataline.addAction("Throughput")
        add_dataline.addAction("Keypresses")
        add_dataline.addAction("System Calls")
        add_dataline.addAction("Mouse Clicks")
        
        #dataline windows actions
        add_dataline.triggered[QAction].connect(self.windowaction)
        adjust = bar.addMenu("Adjust Subwindows")
        adjust.addAction("Tile Layout")
        adjust.triggered[QAction].connect(self.windowaction)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Close Timeline View', 'Are you sure you want to exit?', 
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
            path = os.getcwd()
            os.system("python3 "+ path+"/GUI/Dash/shutdown_dash_server.py")
            print("Server Shutdown")
        else:
            event.ignore()


    def buttonaction(self, b):
        if b == True:
            self.sync_button.setText("Synchronized")
        else:
            self.sync_button.setText("Unsynchronized")

    def windowaction(self, q):
        if q.text() == "New Window":
            sub = QMdiSubWindow()
            sub.resize(700,150)
            sub.setWindowTitle("New Empty Window")
            #sub.setWidget(QTextEdit())
            self.mdi.addSubWindow(sub)
            sub.show()

        if q.text() == "Throughput":
            sub = QMdiSubWindow()
            sub.resize(700,310)
            sub.setWindowTitle("Throughput")
            loading_label = QLabel("Loading...")
            sub.setWidget(loading_label)
            #sub.setWidget(QTextEdit())
            #web = QWebEngineView()
            web = QWebEngineView()
            w = WebEngine(self.throughput_json)
            #df = pd.read_json(self.throughput_json)
            web.load(QUrl("http://127.0.0.1:8050")) #dash app rendered on browser 
            web.show()
            sub.setWidget(web)
            self.mdi.addSubWindow(sub)
            sub.show()

        if q.text() == "Keypresses":
            sub = QMdiSubWindow()
            sub.resize(700,150)
            sub.setWindowTitle("Keypresses")
            sub.setWidget(QTextEdit())

            df = pd.read_json (self.key_json)

            model = pandasModel(df)
            view = QTableView()
            view.setModel(model)

            sub.setWidget(view)

            header = view.horizontalHeader()
            view.setColumnWidth(1, 210)
            header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
            self.mdi.addSubWindow(sub)

            view.show()
            sub.show()

        if q.text() == "System Calls":
            sub = QMdiSubWindow()
            sub.resize(700,150)
            sub.setWindowTitle("System Calls")
            #sub.setWidget(QTextEdit())
            
            df = pd.read_json(self.sys_json)

            model = pandasModel(df)
            view = QTableView()
            view.setModel(model)

            sub.setWidget(view)

            header = view.horizontalHeader()
            view.setColumnWidth(1, 210)
            header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
            self.mdi.addSubWindow(sub)

            view.show()
            sub.show()

        if q.text() == "Mouse Clicks":
            sub = QMdiSubWindow()
            sub.resize(700,150)
            sub.setWindowTitle("Mouse Clicks")
            #sub.setWidget(QTextEdit())
            
            df = pd.read_json (self.mouse_json)

            model = pandasModel(df)
            view = QTableView()
            view.setModel(model)

            sub.setWidget(view)

            header = view.horizontalHeader()
            view.setColumnWidth(1, 210)
            view.setColumnWidth(2, 50)
            header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
            self.mdi.addSubWindow(sub)

            view.show()
            sub.show()

        if q.text() =="Tile Layout":
            self.mdi.tileSubWindows()