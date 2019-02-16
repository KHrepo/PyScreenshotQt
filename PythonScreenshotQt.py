import sys
import time
import datetime
from PyQt5 import QtCore, QtWidgets, QtGui
from PIL import ImageGrab
import numpy as np
import cv2

class CaptureSelectArea(QtWidgets.QWidget):
    def __init__(self, parent):
        super(CaptureSelectArea, self).__init__(parent=None)
        self.parent=parent
        self.parent.showMinimized()
        QtWidgets.QWidget.__init__(self)
        self.screen = QtWidgets.QDesktopWidget().screenGeometry()
        self.setGeometry(0, 0, self.screen.width(), self.screen.height())
        self.setWindowTitle(' ')
        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()
        self.setWindowOpacity(0.5)
        QtWidgets.QApplication.setOverrideCursor(
            QtGui.QCursor(QtCore.Qt.CrossCursor)
        )
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        print("Capture the screen...")
        self.show()

    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        qp.setPen(QtGui.QPen(QtGui.QColor("blue"), 1))
        qp.setBrush(QtGui.QColor(128, 128, 128, 100))
        qp.drawRect(QtCore.QRect(self.begin, self.end))

    def mousePressEvent(self, event):
        self.setMouseTracking(True)
        self.begin = event.pos()
        self.end = self.begin
        self.update()

    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.update()

    def mouseReleaseEvent(self, event):
        QtWidgets.QApplication.setOverrideCursor(
            QtGui.QCursor(QtCore.Qt.ArrowCursor)
        )
        self.close()
        self.parent.showNormal()
        filename = "CaptureImage_"+"{0:%Y-%m-%d_%H-%M-%S}".format(datetime.datetime.now())+".png"

        x1 = min(self.begin.x(), self.end.x())
        y1 = min(self.begin.y(), self.end.y())
        x2 = max(self.begin.x(), self.end.x())
        y2 = max(self.begin.y(), self.end.y())

        img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        img.save(filename)
        img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)

        print("Captured Select Area Image:\n"+filename)
        cv2.imshow(filename, img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.resize(140, 230)
        self.setFixedSize(140, 230)
        self.setWindowTitle("Screenshot Qt")
        select_area_button = QtWidgets.QPushButton("SelectArea", self)
        select_area_button.resize(100,50)
        select_area_button.move(20,30)
        select_area_button.setToolTip("Take the screen of the selected area")  
        select_area_button.clicked.connect(self.press_select_area)
        fullscreen_button = QtWidgets.QPushButton("FullScreen", self)
        fullscreen_button.resize(100,50)
        fullscreen_button.move(20,90)
        fullscreen_button.setToolTip("Take the full screen")
        fullscreen_button.clicked.connect(self.press_fullscreen)
        quit_button = QtWidgets.QPushButton("Quit", self)
        quit_button.resize(100,50)
        quit_button.move(20,150)
        quit_button.setToolTip("Quit the application")
        quit_button.clicked.connect(self.press_quit)

    def press_select_area(self):
        cv2.destroyAllWindows()
        self.select_area = CaptureSelectArea(self)

    def press_fullscreen(self):
        cv2.destroyAllWindows()
        screen = QtWidgets.QDesktopWidget().screenGeometry()

        self.showMinimized()

        time.sleep(0.3)
        filename = "CaptureImage_"+"{0:%Y-%m-%d_%H-%M-%S}".format(datetime.datetime.now())+".png"
        print("Captured FullScreen Image:\n"+filename)
        img = ImageGrab.grab(bbox=(0, 0, screen.width(), screen.height()))
        img.save(filename)
        img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)

        self.showNormal()

        cv2.imshow("Captured FullScreen Image", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def press_quit(self):
        cv2.destroyAllWindows()
        self.close()
        sys.exit()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())