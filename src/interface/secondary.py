'''
Created on Sep 12, 2013

@author: qurban.ali
'''
import site
site.addsitedir(r"R:/Python_Scripts")
from PyQt4.QtGui import *
from PyQt4.QtCore import *

class PaintArea(QLabel):
    def __init__(self, parent = None):
        super(PaintArea, self).__init__(parent)
        pix = QPixmap(r"D:\My\icons & logos\paintDesk\pen\darkYellow.png")
        pix = pix.scaled(100, 100, Qt.KeepAspectRatio)
        cursor = QCursor(pix, 6, 94)
        self.setCursor(cursor)
        self.modified = False
        self.myPenColors = [QColor('green'), QColor('red'), QColor('blue')]
        self.image = QImage()
        self.mouseDown = False
        self.points = []
        self.pix = QPixmap.grabWindow(QApplication.desktop().winId())
        self.pix.save('D:/testImage.png', None, 100)
        self.setStyleSheet("background-image: url(D:/testImage.png)")
        #self.pix2 = QPixmap(self.pix.size())
        #self.pix2.fill(QColor(0, 0, 0, alpha = 100))
        self.pen = QPen(Qt.yellow, 20, Qt.SolidLine)

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
        self.image.fill(qRgb(255, 255, 255))
        self.modified = True
        self.update()
    
    def printImage(self):
        pass
    
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