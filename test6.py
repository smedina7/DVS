import json
import sys
import pandas as pd    
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap, QImage, QIcon
from PyQt5.QtWidgets import QPushButton, QApplication, QTableView, QWidget, QLabel, QHBoxLayout
 
 
class Second(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(Second, self).__init__(parent)
        # self._data = data
        label = QLabel(self)                                                                                                               
        pixmap = QPixmap('test3/Clicks/1602036122.2287035_main.py_root.png')                                                                                                        
        label.setPixmap(pixmap)                                                                                                            
        self.setCentralWidget(label)                                                                                                       
        self.resize(200, 200)
        self.move(300, 200)   
 
 
class First(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(First, self).__init__(parent)
        # self.pushButton = QtWidgets.QPushButton("click me")
        # print(self._data)
 
        # self.setCentralWidget(self.pushButton)
 
        # self.pushButton.clicked.connect(self.on_pushButton_clicked)
        # self.dialogs = list()
       

        keys = ["clicks_id", "content", "type", "classname", "start"]
        labels = keys
        w = QtWidgets.QTableWidget(0, len(labels))
        w.setHorizontalHeaderLabels(labels)
        df = pd.read_json (r'test3/ParsedLogs/MouseClicks.JSON')
        pathclicks = ""

        for ind in df.index:
            c = 0
            clicks_id = str(ind)
            w.insertRow(w.rowCount())
            for j in keys:
                it = QtWidgets.QTableWidgetItem()
                if j == "clicks_id":
                    # it = QtWidgets.QTableWidgetItem()
                    it.setData(QtCore.Qt.DisplayRole, (clicks_id))
                
                elif j == "content":
                    path = (df[j][ind])
                    last = path.split('/')[-1]
                    pathclicks = "GUI/src/Data/test3/Clicks/" + last 
                    # print(pathclicks)
                    # it = QtWidgets.QTableWidgetItem()
                    it.setData(QtCore.Qt.DisplayRole, (pathclicks))
                    icon  = QtGui.QIcon(pathclicks)

                    # btn= QtWidgets.QPushButton('Open')
                    btn= QtWidgets.QPushButton()
                    btn.setIcon(icon)
                    btn.setIconSize(QtCore.QSize(300, 300))
                    w.setCellWidget(ind,c, btn)
                    # self.w.cellClicked.connect(self.on_pushButton_clicked)
                    # button.clicked.connect(lambda: calluser(name))
                    # btn.clicked.connect(lambda: self.on_pushButton_clicked(pathclicks))
                    # self.dialogs = list()
                    btn.clicked.connect(self.on_pushButton_clicked)
                    


                else:
                    # it = QtWidgets.QTableWidgetItem()
                    it.setData(QtCore.Qt.DisplayRole, (df[j][ind]))

                w.setItem(ind, c, it)
                c= c+1


        # icon  = QtGui.QIcon('test3/Clicks/1602036122.2287035_main.py_root.png')

        # btn= QtWidgets.QPushButton('Open')
        # btn= QtWidgets.QPushButton()
        # btn.setIcon(icon)
        # btn.setIconSize(QtCore.QSize(300, 300))
        # w.setCellWidget(0,1, btn)
        # btn.clicked.connect(self.on_pushButton_clicked)
        # btn.clicked.connect(lambda: self.on_pushButton_clicked(pathclicks))
        # self.btn.cellClicked.connect(self.on_pushButton_clicked)
        self.dialogs = list()
        self.setCentralWidget(w)

    def on_pushButton_clicked(self):
        # print("Row %d and Column %d was clicked" % (row, column))
        dialog = Second(self)
        self.dialogs.append(dialog)
        dialog.show()
 
 
def main():
    app = QtWidgets.QApplication(sys.argv)
    main = First()
    main.resize(640, 480)
    main.show()
    sys.exit(app.exec_())
 
if __name__ == '__main__':
    main()