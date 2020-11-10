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
        self.clicks = clicks_path
        label = QLabel(self)                                                                                                              
        pixmap = QPixmap(self.clicks) 
        pixmap4 = pixmap.scaled(1600, 1600, QtCore.Qt.KeepAspectRatio)                                                                                                       
        label.setPixmap(pixmap4)                                                                                                          
        self.setCentralWidget(label)                                                                                                       
        self.resize(200, 200)
        self.move(300, 200)   
 
class Timed(QtWidgets.QMainWindow):
    def __init__(self, data, clicks_path):
        QtWidgets.QMainWindow.__init__(self)
        self._data = data
        dfdata = data
        self.clicks = clicks_path

        keys = ["timed_id","type", "classname", "content", "start"]
        labels = keys
        w = QtWidgets.QTableWidget(0, len(labels))
        w.setHorizontalHeaderLabels(labels)
        df = pd.read_json (dfdata)
        pathclicks = ""
        
        for ind in df.index:
            c = 0
            clicks_id = str(ind)
            w.insertRow(w.rowCount())
            
            for j in keys:
                btn= QtWidgets.QPushButton()
                it = QtWidgets.QTableWidgetItem()
                if j == "timed_id":
                    it.setData(QtCore.Qt.DisplayRole, (clicks_id))
                
                elif j == "content":
                    path = (df[j][ind])
                    last = path.split('/')[-1]
                    pathclicks = os.path.join(self.clicks, last)
                    icon  = QtGui.QIcon(pathclicks)
                    btn= QtWidgets.QPushButton()
                    btn.setIcon(icon)
                    btn.setIconSize(QtCore.QSize(200, 200))
                    btn.setStyleSheet('QPushButton{border: 0px solid;}')
                    w.setCellWidget(ind,c, btn)
                    btn.clicked.connect(lambda: self.on_pushButton_clicked(pathclicks))

                else:
                    it.setData(QtCore.Qt.DisplayRole, (df[j][ind]))

                w.setItem(ind, c, it)
                c= c+1

        btn.clicked.connect(lambda: self.on_pushButton_clicked(pathclicks))
        self.dialogs = list()
        w.resizeColumnsToContents()
        w.resizeRowsToContents()
        self.setCentralWidget(w)

    def on_pushButton_clicked(self, clicks_path):
        self.clicks = clicks_path
        dialog = Second(self.clicks,self)
        self.dialogs.append(dialog)
        dialog.show()
 