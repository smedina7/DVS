import json
import sys
import os
import pandas as pd    
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap, QImage, QIcon
from PyQt5.QtCore import QAbstractTableModel, Qt
from PyQt5.QtWidgets import QTableWidget, QPushButton, QApplication, QTableView, QWidget, QLabel, QHBoxLayout
 
 
class Second(QtWidgets.QMainWindow):
    def __init__(self, clicks_path, parent=None):
        super(Second, self).__init__(parent)
        self.clicks = clicks_path
        label = QLabel(self)                                                                                                              
        pixmap = QPixmap(self.clicks) 
        pixmap4 = pixmap.scaled(1600, 1600, QtCore.Qt.KeepAspectRatio)                                                                                                       
        label.setPixmap(pixmap4)
        title = self.clicks
        self.setWindowTitle(title)                                                                                                           
        self.setCentralWidget(label)                                                                                                       
        self.resize(200, 200)
        self.move(300, 200)   
 
class Timed(QTableWidget):
    def __init__(self, data, clicks_path, *args):
        QTableWidget.__init__(self, *args)
        self._data = data
        dfdata = data
        self.clicks = clicks_path

        keys = ["timed_id","type", "classname", "content", "start"]
        labels = keys
        self.setHorizontalHeaderLabels(labels)
        df = pd.read_json (dfdata)
        pathclicks = ""
        
        for ind in df.index:
            c = 0
            clicks_id = str(ind)
            self.insertRow(self.rowCount())
            
            for j in keys:
                it = QtWidgets.QTableWidgetItem()
                if j == "timed_id":
                    it.setData(QtCore.Qt.DisplayRole, (clicks_id))
                
                elif j == "content":
                    path = (df[j][ind])
                    last = path.split('/')[-1]
                    pathclicks = os.path.join(self.clicks, last)
                    icon  = QtGui.QIcon(pathclicks)
                    self.btn= QtWidgets.QToolButton()
                    self.btn.setText(pathclicks)
                    self.btn.setIcon(icon)
                    self.btn.setIconSize(QtCore.QSize(200, 200))
                    self.btn.setStyleSheet('QToolButton{border: 0px solid; font-size: 1px;padding-bottom: 1px; height: 100px; width: 200px;}')
                    self.setCellWidget(ind,c,self.btn)
                    self.btn.clicked.connect(lambda: self.on_pushButton_clicked(pathclicks))

                else:
                    it.setData(QtCore.Qt.DisplayRole, (df[j][ind]))

                self.setItem(ind, c, it)
                c= c+1

       
        self.dialogs = list()
        self.resizeColumnsToContents()
        self.resizeRowsToContents()

    def on_pushButton_clicked(self, clicks_path):
        self.clicks = clicks_path
        path = self.sender().text()
        dialog = Second(path,self)
        self.dialogs.append(dialog)
        dialog.show()