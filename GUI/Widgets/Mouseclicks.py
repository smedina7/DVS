import json
import sys
import os
import pandas as pd    
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap, QImage, QIcon
from PyQt5.QtCore import QAbstractTableModel, Qt
from PyQt5.QtWidgets import QPushButton, QApplication, QTableView, QWidget, QLabel, QHBoxLayout
 
 
class Second(QtWidgets.QMainWindow):
    def __init__(self, clicks_path, parent=None):
        super(Second, self).__init__(parent)
        # self._data = data
        self.clicks = clicks_path
        # print("Window2", self.clicks)
        label = QLabel(self)                                                                                                               
        # pixmap = QPixmap('test3/Clicks/1602036122.2287035_main.py_root.png') 
        pixmap = QPixmap(self.clicks) 
        pixmap4 = pixmap.scaled(1600, 1600, QtCore.Qt.KeepAspectRatio)                                                                                                       
        label.setPixmap(pixmap4)                                                                                                          
        self.setCentralWidget(label)                                                                                                       
        self.resize(200, 200)
        self.move(300, 200)   
 
 
class First(QtWidgets.QMainWindow):
    def __init__(self, data, clicks_path):
        # super(First, self).__init__(parent)
        QtWidgets.QMainWindow.__init__(self)
        self._data = data
        dfdata = data
        self.clicks = clicks_path

        # print("DF", dfdata)


        keys = ["clicks_id", "content", "type", "classname", "start"]
        labels = keys
        w = QtWidgets.QTableWidget(0, len(labels))
        w.setHorizontalHeaderLabels(labels)
        # df = pd.read_json (r'test3/ParsedLogs/MouseClicks.JSON')
        df = pd.read_json (dfdata)
        pathclicks = ""
        
        for ind in df.index:
            c = 0
            clicks_id = str(ind)
            w.insertRow(w.rowCount())
            
            for j in keys:
                btn= QtWidgets.QPushButton()
                it = QtWidgets.QTableWidgetItem()
                if j == "clicks_id":
                    it.setData(QtCore.Qt.DisplayRole, (clicks_id))
                
                elif j == "content":
                    path = (df[j][ind])
                    last = path.split('/')[-1]
                    # pathclicks = "test3/Clicks/" + last 
                    pathclicks = os.path.join(self.clicks, last)
                    # print("Pathclicks", self.clicks, last)
                    it.setData(QtCore.Qt.DisplayRole, (pathclicks))
                    icon  = QtGui.QIcon(pathclicks)
                    btn= QtWidgets.QPushButton()
                    btn.setIcon(icon)
                    btn.setIconSize(QtCore.QSize(300, 300))
                    w.setCellWidget(ind,c, btn)
                    # btn.clicked.connect(self.on_pushButton_clicked(pathclicks))
                    # btn.clicked.connect(self.on_pushButton_clicked)
                    btn.clicked.connect(lambda: self.on_pushButton_clicked(pathclicks))


                else:
                    it.setData(QtCore.Qt.DisplayRole, (df[j][ind]))

                # btn.clicked.connect(lambda: self.on_pushButton_clicked(pathclicks))
                w.setItem(ind, c, it)
                c= c+1


        


        btn.clicked.connect(lambda: self.on_pushButton_clicked(pathclicks))
        self.dialogs = list()
        self.setCentralWidget(w)

    def on_pushButton_clicked(self, clicks_path):
        self.clicks = clicks_path
        # print("push button", self.clicks)
        dialog = Second(self.clicks,self)
        self.dialogs.append(dialog)
        dialog.show()
 
 