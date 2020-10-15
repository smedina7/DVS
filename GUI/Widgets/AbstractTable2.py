import sys
import os
from PyQt5.QtWidgets import QTableView
from PyQt5.QtCore import QAbstractTableModel, Qt
##from PyQt5.QtGui     import *
# from PyQt5.QtGui     import *
# from PyQt5.QtCore    import *
# from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt

class pandasModel2(QAbstractTableModel):

    def __init__(self, data, clicks_path):
        QAbstractTableModel.__init__(self)
        self._data = data
        self.clicks = clicks_path

    def rowCount(self, parent=None):
        #the return is an int num of rows found in json file
        return self._data.shape[0]

    def columnCount(self, parent=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        pathclicks = ""
        if index.isValid():
            if role == Qt.DisplayRole:
                if index.column() == 1:
                    # self.setIcon(QIcon("test3/Clicks/1602036122.2287035_main.py_root.png"))
                    path = self._data.iloc[index.row(), index.column()]
                    # return QtGui.QColor('red')
                    last = path.split('/')[-1]
                    #pathclicks = "GUI/src/Data/test3/Clicks/" + last 
                    pathclicks = os.path.join(self.clicks, last)

                    # return str (pathclicks)
                else: 
                    return str(self._data.iloc[index.row(), index.column()])

            #if role == Qt.BackgroundRole and index.column() == 1:
                # See below for the data structure.
              #  return QtGui.QColor('blue')
            
            if role == Qt.DecorationRole and index.column() == 1:
                # pathclicks = "GUI/src/Data/test3/Clicks/" + last 
                # return QtGui.QIcon("GUI/src/Data/test3/Clicks/1602036122.2287035_main.py_root.png")
                path = self._data.iloc[index.row(), index.column()]
                    # return QtGui.QColor('red')
                last = path.split('/')[-1]
                #pathclicks = "GUI/src/Data/test3/Clicks/" + last 
                pathclicks = os.path.join(self.clicks, last)
                return QtGui.QIcon(pathclicks)
            
            return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        return None


class pandasModel3(QAbstractTableModel):

    def __init__(self, data, timed_path):
        QAbstractTableModel.__init__(self)
        self._data = data
        self.timed = timed_path

    def rowCount(self, parent=None):
        #the return is an int num of rows found in json file
        return self._data.shape[0]

    def columnCount(self, parent=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        pathclicks = ""
        if index.isValid():
            if role == Qt.DisplayRole:
                if index.column() == 3:
                    path = self._data.iloc[index.row(), index.column()]
                    last = path.split('/')[-1]
                    #pathclicks = "GUI/src/Data/test3/Timed/" + last 
                    pathclicks = os.path.join(self.timed, last)

                    #return str (pathclicks)
                else: 
                    return str(self._data.iloc[index.row(), index.column()])

            
            if role == Qt.DecorationRole and index.column() == 3:
                path = self._data.iloc[index.row(), index.column()]
                last = path.split('/')[-1]
                #pathclicks = "GUI/src/Data/test3/Timed/" + last 
                pathclicks = os.path.join(self.timed, last)
                return QtGui.QIcon(pathclicks)
            
            return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        return None