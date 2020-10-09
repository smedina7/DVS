import sys
from PyQt5.QtGui     import *
from PyQt5.QtCore    import *
from PyQt5.QtWidgets import *

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setGeometry(600, 200, 330, 180)

        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(3)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(['Product', 'Description', 'Screenshots'])
        self.setCentralWidget(self.tableWidget)


        for x in range(3):
            self.button = QPushButton('', self) 
            self.button.setFlat(True)
            self.tableWidget.setItem(x, 0, QTableWidgetItem('Product{}'.format(x)))
            self.tableWidget.setItem(x, 1, QTableWidgetItem('Description'))
            self.tableWidget.setCellWidget(x, 2, self.button)

            self.button.clicked.connect(
                lambda state, w=self.tableWidget.cellWidget(x,2), r=x, c=2: self.button_pushed(w, r, c)
            )



    def button_pushed(self, w, r, c): 
        w.setIcon(QIcon("test3/Clicks/1602036122.2287035_main.py_root.png"))
        # if w.text() != "Likes/UnLikes":
        #     w.setIcon(QIcon(""))
        #     w.setText("Likes/UnLikes")
        # else:
        #     w.setIcon(QIcon("test3/Clicks/1602036122.2287035_main.py_root.png"))
        #     w.setText(" Likes")

        if w.text() != "Enabled":
           
            w.setText("")
        else:
            # w.setIcon(QIcon("test3/Clicks/1602036122.2287035_main.py_root.png"))
            w.setText("Enabled")
            self.showMaximized()


        w.setIconSize(QSize(100, 100))
        self.tableWidget.setCellWidget(r, c, w)

app = QApplication(sys.argv)
w   = MainWindow()
w.show()
sys.exit(app.exec_())