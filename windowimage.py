import cv2
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QPixmap, QImage
 

class NewImage(QWidget):

    def __init__(self, npImage):
        super().__init__()
        label = QLabel(self)
        pixmap = self.ConvertNumpyToQPixmap(npImage)
        label.setPixmap(pixmap)
        self.resize(pixmap.width(), pixmap.height())
        self.show()

    @staticmethod
    def ConvertNumpyToQPixmap(np_img):
        height, width, channel = np_img.shape
        bytesPerLine = 3 * width
        return QPixmap(QImage(np_img.data, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    currentNumpyImage = cv2.imread("test3/Clicks/1602036122.2287035_main.py_root.png")
    window = NewImage(currentNumpyImage)
    sys.exit(app.exec_())