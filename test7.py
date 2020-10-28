import sys
import pandas as pd
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt

df = pd.read_json (r'test3/ParsedLogs/MouseClicks.JSON')

class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
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


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.table = QtWidgets.QTableView()

        # data = [
        #   [4, 9, 2],
        #   [1, 0, 0],
        #   [3, 5, 0],
        #   [3, 3, 2],
        #   [7, 8, 9],
        # ]

        self.model = TableModel(df)
        self.table.setModel(self.model)
        

        self.setCentralWidget(self.table)
        self.pushButton = QtWidgets.QPushButton("click me")


app=QtWidgets.QApplication(sys.argv)
window=MainWindow()
window.show()
app.exec_()