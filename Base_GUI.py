# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Layers_4.ui'
##
## Created by: Qt User Interface Compiler version 6.6.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt, Signal, QEvent)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QFrame, QHBoxLayout,
    QHeaderView, QLabel, QMainWindow, QPushButton,
    QSizePolicy, QStackedWidget, QStatusBar, QTreeWidget,
    QTreeWidgetItem, QVBoxLayout, QWidget)

class CustomTreeWidget(QTreeWidget):

    itemsReordered = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setDragDropMode(QTreeWidget.InternalMove)
    
    def dropEvent(self, event):
        super().dropEvent(event)
        self.itemsReordered.emit()
        
        self.onItemsReordered()
    
    def onItemsReordered(self):
        pass
        #print("Items have been reordered.")

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1000, 600)
        #MainWindow.setMinimumSize(QSize(1000, 600))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout_3 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.frame_4 = QFrame(self.centralwidget)
        self.frame_4.setObjectName(u"frame_4")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_4.sizePolicy().hasHeightForWidth())
        self.frame_4.setSizePolicy(sizePolicy)
        self.frame_4.setFrameShape(QFrame.NoFrame)
        self.frame_4.setFrameShadow(QFrame.Plain)
        self.frame_4.setLineWidth(0)
        self.horizontalLayout = QHBoxLayout(self.frame_4)
        self.horizontalLayout.setSpacing(1)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.frame_2 = QFrame(self.frame_4)
        self.frame_2.setObjectName(u"frame_2")
        sizePolicy.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy)
        self.frame_2.setFrameShape(QFrame.NoFrame)
        self.frame_2.setFrameShadow(QFrame.Plain)
        self.frame_2.setLineWidth(0)
        self.verticalLayout_2 = QVBoxLayout(self.frame_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.imageLabel = QLabel(self.frame_2)
        self.imageLabel.setObjectName(u"imageLabel")
        sizePolicy.setHeightForWidth(self.imageLabel.sizePolicy().hasHeightForWidth())
        self.imageLabel.setSizePolicy(sizePolicy)
        self.imageLabel.setScaledContents(False)

        self.verticalLayout_2.addWidget(self.imageLabel)

        self.openImageButton = QPushButton(self.frame_2)
        self.openImageButton.setObjectName(u"openImageButton")

        self.verticalLayout_2.addWidget(self.openImageButton)


        self.horizontalLayout.addWidget(self.frame_2)

        self.frame = QFrame(self.frame_4)
        self.frame.setObjectName(u"frame")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy1)
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Plain)
        self.frame.setLineWidth(1)
        self.verticalLayout = QVBoxLayout(self.frame)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.treeWidgetLayers = CustomTreeWidget(self.frame)
        self.treeWidgetLayers.setObjectName(u"treeWidgetLayers")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.treeWidgetLayers.sizePolicy().hasHeightForWidth())
        self.treeWidgetLayers.setSizePolicy(sizePolicy2)
        self.treeWidgetLayers.setDragDropMode(QAbstractItemView.InternalMove)

        self.verticalLayout.addWidget(self.treeWidgetLayers)

        self.frame_3 = QFrame(self.frame)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.NoFrame)
        self.frame_3.setFrameShadow(QFrame.Plain)
        self.frame_3.setLineWidth(0)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_3)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(5, 3, 5, 3)
        self.button_addLayer = QPushButton(self.frame_3)
        self.button_addLayer.setObjectName(u"button_addLayer")

        self.horizontalLayout_2.addWidget(self.button_addLayer)

        self.button_removeLayer = QPushButton(self.frame_3)
        self.button_removeLayer.setObjectName(u"button_removeLayer")

        self.horizontalLayout_2.addWidget(self.button_removeLayer)


        self.verticalLayout.addWidget(self.frame_3)

        self.stackedWidget = QStackedWidget(self.frame)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.stackedWidget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.stackedWidget.addWidget(self.page_2)

        self.verticalLayout.addWidget(self.stackedWidget)

        self.pushButtonExport = QPushButton(self.frame)
        self.pushButtonExport.setObjectName(u"pushButtonExport")

        self.verticalLayout.addWidget(self.pushButtonExport, alignment=Qt.AlignHCenter)


        self.horizontalLayout.addWidget(self.frame)


        self.horizontalLayout_3.addWidget(self.frame_4)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.imageLabel.setText("")
        self.openImageButton.setText(QCoreApplication.translate("MainWindow", u"Open Image", None))
        ___qtreewidgetitem = self.treeWidgetLayers.headerItem()
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("MainWindow", u"Layers", None));
        self.button_addLayer.setText(QCoreApplication.translate("MainWindow", u"Add Layer", None))
        self.button_removeLayer.setText(QCoreApplication.translate("MainWindow", u"Remove Layer", None))
        self.pushButtonExport.setText(QCoreApplication.translate("MainWindow", u"Export Image", None))
    # retranslateUi

