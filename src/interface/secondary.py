'''
Created on Sep 12, 2013

@author: qurban.ali
'''
import site
site.addsitedir(r"R:/Python_Scripts")
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import uic
from .logic import utilities as util
modulePath = util.modulePath(__name__)
root = util.dirname(util.dirname(util.dirname(modulePath)))
penPath = r"%s\icons\pen"%root

class PaintArea(QLabel):
    def __init__(self, parent = None):
        super(PaintArea, self).__init__(parent)
        self.modified = False
        self.image = QImage()
        self.mouseDown = False
        self.points = []
        self.pix = QPixmap.grabWindow(QApplication.desktop().winId())
        self.pix.save('D:/testImage.png', None, 100)
        self.setStyleSheet("background-image: url(D:/testImage.png)")
        self.colors = {'White': Qt.white, 'Black': Qt.black, 'Red': Qt.red,
              'Dark Red': Qt.darkRed, 'Green': Qt.green,
              'Dark Green': Qt.darkGreen, 'Blue': Qt.blue,
              'Dark Blue': Qt.darkBlue, 'Cyan': Qt.cyan,
              'Dark Cyan': Qt.darkCyan, 'Magenta': Qt.magenta,
              'Dark Magenta': Qt.darkMagenta, 'Yellow': Qt.yellow,
              'Dark Yellow': Qt.darkYellow}
        self.penSize = 2
        self.setPenColor('Yellow')
        self.setPenSize(self.penSize)
        
        
    def penColor(self, color):
        return self.colors[color]
        
    def setPenColor(self, color):
        self.penColor = self.penColor(color)
        self.pen = QPen(self.penColor, self.penSize, Qt.SolidLine)
        imageName = color + ".png"
        path = util.join(penPath, imageName) 
        self.cursorPixmap = QPixmap(path)
    
    def setPenSize(self, size):
        self.penSize = size
        self.pen = QPen(self.penColor, self.penSize, Qt.SolidLine)
        size = int(round(size*4.2 + 12))
        pix = self.cursorPixmap.scaled(size, size, Qt.KeepAspectRatio)
        self.setCursor(QCursor(pix, 0, size))
    
    def undo(self):
        pass

    def saveImage(self):
        painter = QPainter(self.pix)
        painter.setPen(self.pen)
        for i in range(len(self.points)):
            if self.points[i] == '': continue 
            try:
                painter.drawLine(self.points[i], self.points[i+1])
            except: pass
        self.pix.save('D:/My/test/hello.png', None, 100)
    
    def isModified(self):
        return self.modified
    
    def clearImage(self):
        
        self.modified = True
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(self.pen)
        for i in range(len(self.points)):
            if self.points[i] == '': continue 
            try:
                painter.drawLine(self.points[i], self.points[i+1])
            except: pass
        self.update()
    
    def mousePressEvent(self, event):
        self.mouseDown = True
        self.points.append(event.pos())
        self.points.append(event.pos())
        
    def mouseReleaseEvent(self, event):
        self.mouseDown = False
        self.points.append('')
    
    def mouseMoveEvent(self, event):
        if self.mouseDown:
            point = event.pos()
            self.points.append(point)
            
Form, Base = uic.loadUiType('%s\ui\preferences.ui'%root)
class Preferences(Form, Base):
    
    def __init__(self, parentWin = None):
        super(Preferences, self).__init__(parentWin)
        self.setupUi(self)
            
class Menu(QMenu):
    
    def __init__(self, parentWin = None):
        super(Menu, self).__init__(parentWin)
        
def saveDialog():
    pass

def openDialog():
    pass
        
def msgBox(parent, msg = None, btns = QMessageBox.Ok,
           icon = None, ques = None, details = None, title = 'paintDesk'):
    '''
    dispalys the warnings
    @params:
            args: a dictionary containing the following sequence of variables
            {'msg': 'msg to be displayed'[, 'ques': 'question to be asked'],
            'btns': QMessageBox.btn1 | QMessageBox.btn2 | ....}
    '''
    if msg:
        mBox = QMessageBox(parent)
        mBox.setWindowModality(Qt.ApplicationModal)
        mBox.setWindowTitle(title)
        mBox.setText(msg)
        if ques:
            mBox.setInformativeText(ques)
        if icon:
            mBox.setIcon(icon)
        if details:
            mBox.setDetailedText(details)
        mBox.setStandardButtons(btns)
        buttonPressed = mBox.exec_()
        return buttonPressed