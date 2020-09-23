import logging

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class MainGUI(QMainWindow):
    def __init__(self, parent = None):
        logging.debug("MainGUI(): Instantiated")
        super(MainGUI, self).__init__(parent)

        self.mdi = QMdiArea()
        self.setCentralWidget(self.mdi)
        bar = self.menuBar()

        file = bar.addMenu("File")
        file.addAction("New Window")
        file.addAction("Tiled")
        file.triggered[QAction].connect(self.windowaction)

        self.setWindowTitle("Timeline View")

    def windowaction(self, q):
        print("triggered")

        if q.text() == "New Window":
            sub = QMdiSubWindow()
            sub.setWidget(QTextEdit())
            self.mdi.addSubWindow(sub)
            sub.show()
        if q.text() =="Tiled":
            self.mdi.tileSubWindows()

