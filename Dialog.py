from Ui_Dialog import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import cv2
import numpy as np

class Dialog(QDialog, Ui_Dialog):
    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)
        self.update_numeric_fields()
        self.fileName = ""
        self.hMin = 0
        self.sMin = 0
        self.vMax = 0
        self.hMax = 0
        self.sMax = 0
        self.vMax = 0
        self.bind_controls()
        self.fill_camera_select_combobox()
        self.capture = cv2.VideoCapture(0)
        self.success = False

    def fill_camera_select_combobox(self):
        self.comboBox.addItem("0")
        self.comboBox.addItem("1")
        self.comboBox.addItem("2")
        self.comboBox.setCurrentIndex(0)

    def bind_controls(self):
        self.btnFromFile.clicked.connect(self.load_from_file)
        self.btnFromCamera.clicked.connect(self.load_from_camera)
        self.sldHMin.valueChanged.connect(self.update_ui)
        self.sldSMin.valueChanged.connect(self.update_ui)
        self.sldVMin.valueChanged.connect(self.update_ui)
        self.sldHMax.valueChanged.connect(self.update_ui)
        self.sldSMax.valueChanged.connect(self.update_ui)
        self.sldVMax.valueChanged.connect(self.update_ui)

    def load_from_file(self):
        options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog # if you dont like classis open file dialog
        self.fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                       "Jpeg Files (*.jpg)", options=options)
        if self.fileName:
            print(self.fileName)
            self.imgOriginal = cv2.imread(self.fileName)
            self.imgOriginalShow = cv2.cvtColor(self.imgOriginal, cv2.COLOR_BGR2RGB)
            self.imgOriginalShow = cv2.resize(self.imgOriginalShow, (320, 240))

            height, width, channel = self.imgOriginalShow.shape
            bytesPerLine = 3 * width
            convertToQtFormat = QImage(self.imgOriginalShow.data, width, height, bytesPerLine, QImage.Format_RGB888)
            self.lblOriginal.setPixmap(QPixmap.fromImage(convertToQtFormat))

            self.update_ui()

    def load_from_camera(self):
        self.capture = cv2.VideoCapture(self.comboBox.currentIndex())
        self.success, self.imgOriginal = self.capture.read()
        self.success, self.imgOriginal = self.capture.read()
        self.success, self.imgOriginal = self.capture.read() #sometimes one shot is not enough

        if self.success:
            # Load image
            self.imgOriginalShow = cv2.cvtColor(self.imgOriginal, cv2.COLOR_BGR2RGB)
            self.imgOriginalShow = cv2.resize(self.imgOriginalShow, (320, 240))

            height, width, channel = self.imgOriginalShow.shape
            bytesPerLine = 3 * width
            convertToQtFormat = QImage(self.imgOriginalShow.data, width, height, bytesPerLine, QImage.Format_RGB888)
            self.lblOriginal.setPixmap(QPixmap.fromImage(convertToQtFormat))

            self.update_ui()

    def update_ui(self):
        self.update_numeric_fields()
        if self.fileName or self.success:
            # Get current positions of all sliders
            self.hMin = self.sldHMin.value()
            self.sMin = self.sldSMin.value()
            self.vMin = self.sldVMin.value()
            self.hMax = self.sldHMax.value()
            self.sMax = self.sldSMax.value()
            self.vMax = self.sldVMax.value()

            # Set minimum and maximum HSV values to display
            self.lower = np.array([self.hMin, self.sMin, self.vMin])
            self.upper = np.array([self.hMax, self.sMax, self.vMax])

            # Convert to HSV format and color threshold
            self.imgHSV = cv2.cvtColor(self.imgOriginal, cv2.COLOR_BGR2HSV)
            self.imgMask = cv2.inRange(self.imgHSV, self.lower, self.upper)
            self.imgOutput = cv2.bitwise_and(self.imgOriginal, self.imgOriginal, mask=self.imgMask)

            self.imgHSVShow = cv2.resize(self.imgHSV, (320, 240))
            height, width, channel = self.imgHSVShow.shape
            bytesPerLine = 3 * width
            convertToQtFormat = QImage(self.imgHSVShow.data, width, height, bytesPerLine, QImage.Format_RGB888)
            self.lblHSV.setPixmap(QPixmap.fromImage(convertToQtFormat))

            self.imgOutputShow = cv2.cvtColor(self.imgOutput, cv2.COLOR_BGR2RGB)
            self.imgOutputShow = cv2.resize(self.imgOutput, (320, 240))
            height, width, channel = self.imgOutputShow.shape
            bytesPerLine = 3 * width
            convertToQtFormat = QImage(self.imgOutputShow.data, width, height, bytesPerLine, QImage.Format_RGB888)
            self.lblOutput.setPixmap(QPixmap.fromImage(convertToQtFormat))
            #cv2.imshow('result', self.imgOutput)

    def update_numeric_fields(self):
        self.leHMin.setText(str(self.sldHMin.value()))
        self.leSMin.setText(str(self.sldSMin.value()))
        self.leVMin.setText(str(self.sldVMin.value()))
        self.leHMax.setText(str(self.sldHMax.value()))
        self.leSMax.setText(str(self.sldSMax.value()))
        self.leVMax.setText(str(self.sldVMax.value()))
