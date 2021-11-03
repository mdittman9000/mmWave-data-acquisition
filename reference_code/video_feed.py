import cv2
import sys
from PyQt5.QtWidgets import QWidget, QLabel, QApplication
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap

from gui_threads import *

class VideoFrame(QWidget):
    def __init__(self, StreamThread):
        super().__init__()
        self.title = "Video Frame"
        self.initUI(StreamThread)

    @pyqtSlot(QImage)
    def setImage(self, image):
        self.label.setPixmap(QPixmap.fromImage(image))


    def initUI(self, StreamThread):
        self.setWindowTitle(self.title)
        self.setGeometry(10,10,30,30)
        self.resize(360,240)

        self.label=QLabel(self)
        self.label.move(0,0)
        self.label.resize(360,240)

        
        self.classBox = QGroupBox('Class Type')
        
        self.classLayout = QGridLayout()
        self.classLabelCurrentlyRecording = QLabel('')
        self.classLabelCurrentlyRecording.setFont(QFont('Arial',50))
        self.classLayout.addWidget(self.classLabelCurrentlyRecording,0,0)
        self.classBox.setLayout(self.classLayout)

        gridlay = QGridLayout()
        gridlay.addWidget(self.label,0,0)
        gridlay.addWidget(self.classBox, 0,1,1,2)
        self.setLayout(gridlay)

        self.th = StreamThread
        self.th.changePixmap.connect(self.setImage)
        self.th.start()
        self.show()

    def startRecord(self, fileName):
        try:
            self.th.startRecord(fileName)
        except:
            pass

    def stopRecord(self):
        try:
            self.th.stopRecord()
        except:
            pass

            