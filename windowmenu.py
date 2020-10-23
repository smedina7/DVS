import cv2
import sys
from PyQt5 import QtWidgets
from windowimage import NewImage


class Menu(QtWidgets.QMainWindow):

    def __init__(self, numpyPic):
        super().__init__()
        newAct = QtWidgets.QAction('New', self)
        self.numpyPicture = numpyPic
        newAct.triggered.connect(self.newPicture)
        toolbar = self.addToolBar('Exit')
        toolbar.addAction(newAct)
        self.setGeometry(300, 300, 350, 250)
        self.show()

    def newPicture(self):
        #NewImage(self.numpyPicture) #From the previous class  # ---
        self.newImage = NewImage(self.numpyPicture)            # +++


if __name__ == '__main__':
    #currentNumpyImage = cv2.imread("capture.png")
    currentNumpyImage = cv2.imread("logo.png")
    app = QtWidgets.QApplication(sys.argv)
    ex = Menu(currentNumpyImage)
    sys.exit(app.exec_())
