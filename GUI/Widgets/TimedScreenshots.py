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

        keys = ["timed_id","type", "classname", "content","Tag", "start"]
        labels = keys
        self.setHorizontalHeaderLabels(labels)
        df = pd.read_json (dfdata)
        pathclicks = ""
        ser = pd.Series(df['timed_id']) 
        
        for ind in df.index:
            c = 0
            self.insertRow(self.rowCount())
            
            for j in keys:
                it = QtWidgets.QTableWidgetItem()
                if j == "timed_id":
                    tableid = str(ser[ind])
                    it.setData(QtCore.Qt.DisplayRole, (tableid))
                    it.setFlags(QtCore.Qt.ItemIsEnabled)
                
                elif j == "content":
                    path = (df[j][ind])
                    try:
                        last = path.split('/')[-1]
                        pathclicks = os.path.join(self.clicks, last)

                        if QtCore.QFile.exists(pathclicks):
                            it.setData(QtCore.Qt.UserRole, (path))
                        else:
                            it.setData(QtCore.Qt.DisplayRole, (path))
                            
                        icon  = QtGui.QIcon(pathclicks)
                        self.btn= QtWidgets.QToolButton()
                        self.btn.setText(pathclicks)
                        self.btn.setIcon(icon)
                        self.btn.setIconSize(QtCore.QSize(200, 200))
                        self.btn.setStyleSheet('QToolButton{border: 0px solid; font-size: 1px;padding-bottom: 1px; height: 100px; width: 200px;}')
                        self.setCellWidget(ind,c,self.btn)
                        self.btn.clicked.connect(lambda: self.on_pushButton_clicked(pathclicks))
                    
                    except:
                        it.setData(QtCore.Qt.DisplayRole, (path))

                else:
                    it.setData(QtCore.Qt.DisplayRole, (df[j][ind]))
                    it.setFlags(QtCore.Qt.ItemIsEnabled)

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