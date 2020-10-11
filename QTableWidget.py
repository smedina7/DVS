from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication,  QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout
import sys
 
 
class Window(QWidget):
    def __init__(self):
        super().__init__()
 
        self.title = "Keypresses"
        self.top = 100
        self.left = 100
        self.width = 600
        self.height = 400
 
 
        self.InitWindow()
 
 
    def InitWindow(self):
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
 
        self.creatingTables()
 
 
        self.show()

        #d = json.loads(data)
   ##with open('/home/kali/DVS/parsed/pykeylogger/keypressData.JSON') as f:
     ##  data = json.load(f)
    ##d = json.loads(data)
    ##keys = ["keypresses_id", "Content", "Classname", "Start"]

 
    def creatingTables(self):
        self.tableWidget = QTableWidget() 
        self.tableWidget.setRowCount(5)
        self.tableWidget.setColumnCount(4)
 
        self.tableWidget.setItem(0,0, QTableWidgetItem("ID"))
        self.tableWidget.setItem(0,1, QTableWidgetItem("Timestamp"))
        self.tableWidget.setItem(0, 2 , QTableWidgetItem("Log"))
        self.tableWidget.setItem(0, 3 , QTableWidgetItem("Tag"))
 
        self.tableWidget.setItem(1,0, QTableWidgetItem(""))
        self.tableWidget.setItem(1,1, QTableWidgetItem(""))
        self.tableWidget.setItem(1,2, QTableWidgetItem(""))
        self.tableWidget.setColumnWidth(1, 200)
 
        self.tableWidget.setItem(2, 0, QTableWidgetItem(""))
        self.tableWidget.setItem(2, 1, QTableWidgetItem(""))
        self.tableWidget.setItem(2, 2, QTableWidgetItem(""))
 
        self.tableWidget.setItem(3, 0, QTableWidgetItem(""))
        self.tableWidget.setItem(3, 1, QTableWidgetItem(""))
        self.tableWidget.setItem(3, 2, QTableWidgetItem(""))
 
        self.tableWidget.setItem(4, 0, QTableWidgetItem(""))
        self.tableWidget.setItem(4, 1, QTableWidgetItem(""))
        self.tableWidget.setItem(4, 2, QTableWidgetItem(""))
 
        self.vBoxLayout = QVBoxLayout()
        self.vBoxLayout.addWidget(self.tableWidget)
        self.setLayout(self.vBoxLayout)
 
 
App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())