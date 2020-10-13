import logging
import os

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from GUI.Widgets.AbstractTable import pandasModel
from PacketView.Manager import PacketManager
import pandas as pd

class MainGUI(QMainWindow):
    def __init__(self, json_files, parent = None):
        logging.debug("MainGUI(): Instantiated")
        super(MainGUI, self).__init__(parent)
        json_file_list = json_files

        self.key_json = ''
        self.sys_json = ''
        self.mouse_json = ''

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
        add_dataline.addAction("Keypresses")
        add_dataline.addAction("System Calls")
        add_dataline.addAction("Mouse Clicks")

        #dataline windows actions
        add_dataline.triggered[QAction].connect(self.windowaction)
        adjust = bar.addMenu("Adjust Subwindows")
        adjust.addAction("Tile Layout")
        adjust.triggered[QAction].connect(self.windowaction)

        #Get JSON Files
        print(json_file_list)
        
        #get path for each file
        for file in json_file_list:
            print(file)
            if "Keypresses.JSON" in file:
                self.key_json = file
            
            if "SystemCalls.JSON" in file:
                self.sys_json = file
            
            if "MouseClicks.JSON" in file:
                self.mouse_json = file

        print(self.key_json)
        print(self.sys_json)
        print(self.mouse_json)

    #Sync state
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
            sub.setWidget(QTextEdit())
            self.mdi.addSubWindow(sub)
            sub.show()

        if q.text() == "Keypresses":
            sub = QMdiSubWindow()
            sub.resize(700,150)
            sub.setWindowTitle("Keypresses")
            sub.setWidget(QTextEdit())

            if os.path.exists(self.key_json):
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
            else:
                print("NO KEYPRESS JSON FOUND")

        if q.text() == "System Calls":
            sub = QMdiSubWindow()
            sub.resize(700,150)
            sub.setWindowTitle("System Calls")
            sub.setWidget(QTextEdit())
            
            if os.path.exists(self.sys_json):
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
            else:
                print("NO SYSCALLS JSON FOUND")

        if q.text() == "Mouse Clicks":
            sub = QMdiSubWindow()
            sub.resize(700,150)
            sub.setWindowTitle("Mouse Clicks")
            sub.setWidget(QTextEdit())
            
            if os.path.exists(self.mouse_json):
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
            else:
                print("NO MOUSECLICKS JSON FOUND")

        if q.text() =="Tile Layout":
            self.mdi.tileSubWindows()

