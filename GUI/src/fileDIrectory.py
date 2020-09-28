import sys
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
import tkinter as tk
from tkinter import filedialog

class FileDirectory(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.openFileNameDialog()
        self.show()

    def openFileNameDialog(self):
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askdirectory()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FileDirectory()
    sys.exit(app.exec_())