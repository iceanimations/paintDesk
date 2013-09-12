'''
Created on Sep 12, 2013

@author: qurban.ali
'''
import site
site.addsitedir(r"R:/Python_Scripts")
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys
import secondary as sec

class Window(QWidget):
    def __init__(self, parent = None):
        super(Window, self).__init__(parent)
        layout = QStackedLayout()
        self.paintArea = sec.PaintArea(self)
        layout.addWidget(self.paintArea)
        self.setLayout(layout)
        self.setWindowFlags(Qt.MSWindowsFixedSizeDialogHint)
        self.setWindowFlags(Qt.CustomizeWindowHint)
        self.setWindowFlags(Qt.FramelessWindowHint)
        
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
        if event.key() == Qt.Key_S:
            self.paintArea.saveImage()