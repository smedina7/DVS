import sys
# import cv2
# import numpy as np
import pandas as pd
from PyQt5.QtWidgets import QApplication, QTableView, QWidget, QLabel, QHBoxLayout
from PyQt5.QtCore import QAbstractTableModel, Qt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap, QImage
# from PyQt5.QtCore import Qt

df = pd.read_json (r'test3/ParsedLogs/MouseClicks.JSON')

class Second(QtWidgets.QMainWindow,):
    def __init__(self, npImage, parent=None):
        super(Second, self).__init__(parent)
        # hbox = QHBoxLayout(self) 
        # label = QLabel(self)
        # pixmap = QPixmap("test3/Clicks/1602036122.2287035_main.py_root.png")                                                                                                        

        # lbl = QLabel(self)                                                                                                                 
        # lbl.setPixmap(pixmap)                                                                                                              

        # hbox.addWidget(lbl)                                                                                                                
        # self.setLayout(hbox)                                                                                                               

        # # self.move(300, 200)                                                                                                                
        # self.setWindowTitle('Image with PyQt')  
        label = QLabel(self)                                                                                                               
        pixmap = QPixmap('test3/Clicks/1602036122.2287035_main.py_root.png')                                                                                                        
        label.setPixmap(pixmap)                                                                                                            
        self.setCentralWidget(label)                                                                                                       
        self.resize(200, 200)
        self.move(300, 200)      

 
 
class First(QtWidgets.QMainWindow,QAbstractTableModel):
    def __init__(self, data, parent=None):
        super(First, self).__init__(parent)
        QAbstractTableModel.__init__(self)
        self._data = data

        model = pandasModel(df)
        view = QTableView()
        view.setModel(model)
        view.resize(800, 600)
        view.show()

        self.pushButton = QtWidgets.QPushButton("click me")
 
        self.setCentralWidget(self.pushButton)
 
        self.pushButton.clicked.connect(self.on_pushButton_clicked)
        self.dialogs = list()
 
    def on_pushButton_clicked(self):
        # currentNumpyImage = cv2.imread("test3/Clicks/1602036122.2287035_main.py_root.png")
        # window = NewImage(currentNumpyImage)
        dialog = Second(self)
        self.dialogs.append(dialog)
        dialog.show()

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
                    path = self._data.iloc[index.row(), index.column()]
                    last = path.split('/')[-1]
                    pathclicks = "GUI/src/Data/test3/Clicks/" + last 
                else: 
                    return str(self._data.iloc[index.row(), index.column()])
            
            if role == Qt.DecorationRole and index.column() == 1:
                path = self._data.iloc[index.row(), index.column()]
                last = path.split('/')[-1]
                pathclicks = "GUI/src/Data/test3/Clicks/" + last 
                return QtGui.QIcon(pathclicks)
            
            return None

        def headerData(self, col, orientation, role):
            if orientation == Qt.Horizontal and role == Qt.DisplayRole:
                return self._data.columns[col]
            return None


##########################################################
class pandasModel(QAbstractTableModel):

    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parent=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        pathclicks = ""
        if index.isValid():
            if role == Qt.DisplayRole:
                if index.column() == 1:
                    path = self._data.iloc[index.row(), index.column()]
                    last = path.split('/')[-1]
                    pathclicks = "GUI/src/Data/test3/Clicks/" + last 
                else: 
                    return str(self._data.iloc[index.row(), index.column()])

            if role == Qt.DecorationRole and index.column() == 1:
                path = self._data.iloc[index.row(), index.column()]
                last = path.split('/')[-1]
                pathclicks = "GUI/src/Data/test3/Clicks/" + last 
                
                return QtGui.QIcon(pathclicks)
            
            return None
    

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        return None



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    # currentNumpyImage = cv2.imread("est3/Clicks/1602036122.2287035_main.py_root.png")
    # window = NewImage(currentNumpyImage)
    main = First(df)
    main.show()
    # model2 = First(df)
    # main = QTableView()
    # main.setModel(model2)
    # main.show()

    
    
  


    ########################
    model = pandasModel(df)
    view = QTableView()
    view.setModel(model)
    view.resize(800, 600)
    view.show()
    sys.exit(app.exec_())