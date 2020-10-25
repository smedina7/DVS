import logging
import os
import time
import subprocess
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from PyQt5.QtWebEngineWidgets import *
from GUI.Widgets.AbstractTable import pandasModel
from GUI.Widgets.AbstractTable2 import pandasModel2
from GUI.Widgets.AbstractTable2 import pandasModel3

import pandas as pd

class MainGUI(QMainWindow):
    def __init__(self, json_files, clicks, timed, manager_inst, parent = None):
        logging.debug("MainGUI(): Instantiated")
        super(MainGUI, self).__init__(parent)
        json_file_list = json_files
        #throughput_files = throughput_path
        self.clicks_path = clicks
        self.timed_path = timed
        self.manager_instance = manager_inst

        self.key_json = ''
        self.sys_json = ''
        self.mouse_json = ''
        self.throughput_json = ''
        self.timed_json = ''

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
        self.setMinimumHeight(565)
        self.setMinimumWidth(710)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Close Timeline View', 'Are you sure you want to exit?', 
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
            #self.manager_instance.closeWebEngine()
            path = os.getcwd()
            os.system("python3 "+ path+"/GUI/Dash/shutdown_dash_server.py")
            print("Server Shutdown")
        else:
            event.ignore()

    def buttonaction(self, b):
        if b == True:
            self.sync_button.setText("Synchronized")
            for i in self.mdi.subWindowList():
                print(i)
        else:
            self.sync_button.setText("Unsynchronized")


    def resizeEvent(self, event):
        self.sizeHint()

    def windowaction(self, q):
        if q.text() == "Throughput":
            sub = QMdiSubWindow()
            sub.resize(700,310)

            progressBarWidget = QWidget()
            layout = QVBoxLayout()

            pbar = QProgressBar(self)
            pbar.setGeometry(30, 40, 200, 25)
            pbar.setValue(50)
            pbar.setWindowTitle("Loading")

            label = QLabel('Processing, please wait...')
            label.setAlignment(Qt.AlignCenter)

            layout.addWidget(label)
            layout.addWidget(pbar)

            progressBarWidget.setLayout(layout)
            
            sub.setWindowTitle("Throughput")
            loading_label = QLabel("Loading...")
            sub.setWidget(loading_label)
            web = QWebEngineView()
            self.manager_instance.runWebEngine()
            web.load(QUrl("http://127.0.0.1:8050/throughput")) #dash app rendered on browser 
            # web.load(QUrl("http://127.0.0.1:8050/keypresses")) #dash app rendered on browser 
            self.mdi.addSubWindow(sub)
            sub.show()

            sub.setWidget(progressBarWidget)

            pbar.show()
            for i in range(101): 
                # slowing down the loop 
                time.sleep(0.02) 
                # setting value to progress bar 
                pbar.setValue(i) 
            
            pbar.hide()
            sub.setWidget(web)
            web.show()
        
        if q.text() == "Keypresses":
            sub = QMdiSubWindow()
            sub.resize(700,310)

            progressBarWidget = QWidget()
            layout = QVBoxLayout()

            pbar = QProgressBar(self)
            pbar.setGeometry(30, 40, 200, 25)
            pbar.setValue(50)
            pbar.setWindowTitle("Loading")

            label = QLabel('Processing, please wait...')
            label.setAlignment(Qt.AlignCenter)

            layout.addWidget(label)
            layout.addWidget(pbar)

            progressBarWidget.setLayout(layout)
            
            sub.setWindowTitle("Keypresses")
            loading_label = QLabel("Loading...")
            sub.setWidget(loading_label)
            web = QWebEngineView()
            self.manager_instance.runWebEngine()
            web.load(QUrl("http://127.0.0.1:8050/keypresses")) #dash app rendered on browser 
            self.mdi.addSubWindow(sub)
            sub.show()

            sub.setWidget(progressBarWidget)

            pbar.show()
            for i in range(101): 
                # slowing down the loop 
                time.sleep(0.02) 
                # setting value to progress bar 
                pbar.setValue(i) 
            
            pbar.hide()
            sub.setWidget(web)
            web.show()

        # if q.text() == "Keypresses":
        #     sub = QMdiSubWindow()
        #     sub.resize(700,150)

        #     sub.setWindowTitle("Keypresses")
        #     sub.setWidget(QTextEdit())

        #     df = pd.read_json (self.key_json)

        #     model = pandasModel(df)
        #     view = QTableView()
        #     view.setModel(model)

        #     sub.setWidget(view)

        #     header = view.horizontalHeader()
        #     view.setColumnWidth(1, 210)
        #     header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        #     self.mdi.addSubWindow(sub)

        #     view.show()
        #     sub.show()
        
        if q.text() == "System Calls":
            sub = QMdiSubWindow()
            sub.resize(700,310)

            progressBarWidget = QWidget()
            layout = QVBoxLayout()

            pbar = QProgressBar(self)
            pbar.setGeometry(30, 40, 200, 25)
            pbar.setValue(50)
            pbar.setWindowTitle("Loading")

            label = QLabel('Processing, please wait...')
            label.setAlignment(Qt.AlignCenter)

            layout.addWidget(label)
            layout.addWidget(pbar)

            progressBarWidget.setLayout(layout)
            
            sub.setWindowTitle("System Calls")
            loading_label = QLabel("Loading...")
            sub.setWidget(loading_label)
            web = QWebEngineView()
            self.manager_instance.runWebEngine()
            web.load(QUrl("http://127.0.0.1:8050/systemCalls")) #dash app rendered on browser 
            self.mdi.addSubWindow(sub)
            sub.show()

            sub.setWidget(progressBarWidget)

            pbar.show()
            for i in range(101): 
                # slowing down the loop 
                time.sleep(0.02) 
                # setting value to progress bar 
                pbar.setValue(i) 
            
            pbar.hide()
            sub.setWidget(web)
            web.show()

        # if q.text() == "System Calls":
        #     sub = QMdiSubWindow()
        #     sub.resize(700,150)
        #     sub.setWindowTitle("System Calls")
        #     #sub.setWidget(QTextEdit())
            
        #     df = pd.read_json(self.sys_json)

        #     model = pandasModel(df)
        #     view = QTableView()
        #     view.setModel(model)

        #     sub.setWidget(view)

        #     header = view.horizontalHeader()
        #     view.setColumnWidth(1, 210)
        #     header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        #     self.mdi.addSubWindow(sub)

        #     view.show()
        #     sub.show()


        if q.text() == "Mouse Clicks":
            sub = QMdiSubWindow()
            sub.resize(700,310)

            progressBarWidget = QWidget()
            layout = QVBoxLayout()

            pbar = QProgressBar(self)
            pbar.setGeometry(30, 40, 200, 25)
            pbar.setValue(50)
            pbar.setWindowTitle("Loading")

            label = QLabel('Processing, please wait...')
            label.setAlignment(Qt.AlignCenter)

            layout.addWidget(label)
            layout.addWidget(pbar)

            progressBarWidget.setLayout(layout)
            
            sub.setWindowTitle("Mouse Clicks")
            loading_label = QLabel("Loading...")
            sub.setWidget(loading_label)
            web = QWebEngineView()
            self.manager_instance.runWebEngine()
            web.load(QUrl("http://127.0.0.1:8050/mouseClicks")) #dash app rendered on browser 
            self.mdi.addSubWindow(sub)
            sub.show()

            sub.setWidget(progressBarWidget)

            pbar.show()
            for i in range(101): 
                # slowing down the loop 
                time.sleep(0.02) 
                # setting value to progress bar 
                pbar.setValue(i) 
            
            pbar.hide()
            sub.setWidget(web)
            web.show()

        # if q.text() == "Mouse Clicks":
        #     sub = QMdiSubWindow()
        #     sub.resize(700,150)
        #     sub.setWindowTitle("Mouse Clicks")
        #     sub.setWidget(QTextEdit())
            
        #     df = pd.read_json(self.mouse_json)

        #     model = pandasModel2(df, self.clicks_path)
        #     view = QTableView()
        #     view.setModel(model)

        #     sub.setWidget(view)

        #     header = view.horizontalHeader()
        #     view.setColumnWidth(1, 210)
        #     view.setColumnWidth(2, 50)
        #     view.setIconSize(QSize(256, 256))
        #     header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        #     self.mdi.addSubWindow(sub)

        #     view.show()
        #     sub.show()

        if q.text() == "Timed Screenshots":
            sub = QMdiSubWindow()
            sub.resize(700,150)
            sub.setWindowTitle("Timed Screenshots")
            sub.setWidget(QTextEdit())

            df = pd.read_json(self.timed_json)

            model = pandasModel3(df, self.timed_path)
            view = QTableView()
            view.setModel(model)

            sub.setWidget(view)

            header = view.horizontalHeader()
            view.setColumnWidth(4, 210)
            view.setColumnWidth(2, 50) 
            view.setIconSize(QSize(256, 256))
            header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
            self.mdi.addSubWindow(sub)

            view.show()
            sub.show()

        if q.text() =="Tile Layout":
            self.mdi.tileSubWindows()
        