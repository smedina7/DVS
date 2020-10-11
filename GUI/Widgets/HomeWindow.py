import logging
import os

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from GUI.Widgets.AbstractTable import pandasModel
from GUI.Widgets.AbstractTable2 import pandasModel2
import pandas as pd

class MainGUI(QMainWindow):
    def __init__(self, parent = None):
        logging.debug("MainGUI(): Instantiated")
        super(MainGUI, self).__init__(parent)
        JSON_FILE_DIR = "GUI/src/Data"

        #Set File Paths
        self.key_json = os.path.join(JSON_FILE_DIR, "Keypresses.JSON")
        self.sys_json = os.path.join(JSON_FILE_DIR, "SystemCalls.JSON")
        self.mouse_json = os.path.join(JSON_FILE_DIR, "MouseClicks.JSON")

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
            sub.setWidget(QTextEdit())
            
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
            sub.setWidget(QTextEdit())
            
            
            df = pd.read_json (self.mouse_json)

            model = pandasModel2(df)
            view = QTableView()
            view.setModel(model)

            sub.setWidget(view)
 
            header = view.horizontalHeader()
            view.setColumnWidth(1, 210)

            #change 7 to #rows 
            for x in range(7):
                #print(x)
                view.setRowHeight(x,100)
            
            view.setColumnWidth(2, 50) 
            view.setIconSize(QSize(256, 256))

            
            #############################
            # button = QPushButton('PyQt5 button', sub)
            # button.setToolTip('This is an example button')
            # button.move(100,70)
            #sub.show() 
            #############################
            header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
            self.mdi.addSubWindow(sub)

            view.show()
            sub.show()

        if q.text() =="Tile Layout":
            self.mdi.tileSubWindows()

