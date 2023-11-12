# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.6.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QButtonGroup, QDialog, QGraphicsView,
    QGroupBox, QPushButton, QSizePolicy, QToolButton,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(832, 576)
        Dialog.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.groupBox = QGroupBox(Dialog)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(10, 70, 91, 451))
        self.groupBox.setStyleSheet(u"background-color: rgb(135, 135, 135);")
        self.toolButton_12 = QToolButton(self.groupBox)
        self.toolButton_12.setObjectName(u"toolButton_12")
        self.toolButton_12.setGeometry(QRect(50, 130, 21, 22))
        self.toolButton_10 = QToolButton(self.groupBox)
        self.toolButton_10.setObjectName(u"toolButton_10")
        self.toolButton_10.setGeometry(QRect(50, 70, 21, 22))
        self.toolButton = QToolButton(self.groupBox)
        self.toolButton.setObjectName(u"toolButton")
        self.toolButton.setGeometry(QRect(20, 40, 21, 22))
        icon = QIcon(QIcon.fromTheme(u"edit-delete"))
        self.toolButton.setIcon(icon)
        self.toolButton_9 = QToolButton(self.groupBox)
        self.toolButton_9.setObjectName(u"toolButton_9")
        self.toolButton_9.setGeometry(QRect(20, 70, 21, 22))
        self.toolButton_11 = QToolButton(self.groupBox)
        self.toolButton_11.setObjectName(u"toolButton_11")
        self.toolButton_11.setGeometry(QRect(20, 130, 21, 22))
        self.toolButton_8 = QToolButton(self.groupBox)
        self.toolButton_8.setObjectName(u"toolButton_8")
        self.toolButton_8.setGeometry(QRect(20, 100, 21, 22))
        self.toolButton_2 = QToolButton(self.groupBox)
        self.toolButton_2.setObjectName(u"toolButton_2")
        self.toolButton_2.setGeometry(QRect(50, 40, 21, 22))
        self.toolButton_7 = QToolButton(self.groupBox)
        self.toolButton_7.setObjectName(u"toolButton_7")
        self.toolButton_7.setGeometry(QRect(50, 100, 21, 22))
        self.graphicsView = QGraphicsView(Dialog)
        self.graphicsView.setObjectName(u"graphicsView")
        self.graphicsView.setGeometry(QRect(110, 80, 621, 451))
        self.pushButton_2 = QPushButton(Dialog)
        self.buttonGroup = QButtonGroup(Dialog)
        self.buttonGroup.setObjectName(u"buttonGroup")
        self.buttonGroup.addButton(self.pushButton_2)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(740, 80, 75, 24))
        self.pushButton_3 = QPushButton(Dialog)
        self.buttonGroup.addButton(self.pushButton_3)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setGeometry(QRect(740, 140, 75, 24))
        self.pushButton_4 = QPushButton(Dialog)
        self.buttonGroup.addButton(self.pushButton_4)
        self.pushButton_4.setObjectName(u"pushButton_4")
        self.pushButton_4.setGeometry(QRect(740, 110, 75, 24))
        self.groupBox_2 = QGroupBox(Dialog)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setGeometry(QRect(110, 10, 521, 61))
        self.groupBox_2.setStyleSheet(u"background-color: rgb(207, 207, 207);")
        self.toolButton_3 = QToolButton(self.groupBox_2)
        self.toolButton_3.setObjectName(u"toolButton_3")
        self.toolButton_3.setGeometry(QRect(10, 20, 21, 21))
        self.toolButton_3.setStyleSheet(u"background-image: url(:/newPrefix/icons/zoom_in.png);")
        icon1 = QIcon()
        iconThemeName = u"applications-science"
        if QIcon.hasThemeIcon(iconThemeName):
            icon1 = QIcon.fromTheme(iconThemeName)
        else:
            icon1.addFile(u".", QSize(), QIcon.Normal, QIcon.Off)

        self.toolButton_3.setIcon(icon1)
        self.toolButton_4 = QToolButton(self.groupBox_2)
        self.toolButton_4.setObjectName(u"toolButton_4")
        self.toolButton_4.setGeometry(QRect(40, 20, 21, 22))

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.groupBox.setTitle(QCoreApplication.translate("Dialog", u"Tools", None))
        self.toolButton_12.setText(QCoreApplication.translate("Dialog", u"...", None))
        self.toolButton_10.setText(QCoreApplication.translate("Dialog", u"...", None))
        self.toolButton.setText(QCoreApplication.translate("Dialog", u"...", None))
        self.toolButton_9.setText(QCoreApplication.translate("Dialog", u"...", None))
        self.toolButton_11.setText(QCoreApplication.translate("Dialog", u"...", None))
        self.toolButton_8.setText(QCoreApplication.translate("Dialog", u"...", None))
        self.toolButton_2.setText(QCoreApplication.translate("Dialog", u"...", None))
        self.toolButton_7.setText(QCoreApplication.translate("Dialog", u"...", None))
        self.pushButton_2.setText(QCoreApplication.translate("Dialog", u"Upload", None))
        self.pushButton_3.setText(QCoreApplication.translate("Dialog", u"Cancel", None))
        self.pushButton_4.setText(QCoreApplication.translate("Dialog", u"Save", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Dialog", u"image editor", None))
        self.toolButton_3.setText(QCoreApplication.translate("Dialog", u"...", None))
        self.toolButton_4.setText(QCoreApplication.translate("Dialog", u"...", None))
    # retranslateUi

