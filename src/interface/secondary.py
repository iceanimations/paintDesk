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
    def __init__(self, parentWin = None):
        super(PaintArea, self).__init__(parentWin)
        self.parentWin = parentWin
        self.modified = False
        self.image = QImage()
        self.mouseDown = False
        self.points = []
        self.pix = QPixmap.grabWindow(QApplication.desktop().winId())
        self.colors = {'White': Qt.white, 'Black': Qt.black, 'Red': Qt.red,
              'Dark Red': Qt.darkRed, 'Green': Qt.green,
              'Dark Green': Qt.darkGreen, 'Blue': Qt.blue,
              'Dark Blue': Qt.darkBlue, 'Cyan': Qt.cyan,
              'Dark Cyan': Qt.darkCyan, 'Magenta': Qt.magenta,
              'Dark Magenta': Qt.darkMagenta, 'Yellow': Qt.yellow,
              'Dark Yellow': Qt.darkYellow}
        self.penSize = 3
        self.setPenColor('Black')
        self.start = self.end = None
        
    def setPenColor(self, color):
        self.penColor = self.colors[color]
        self.pen = QPen(self.penColor, self.penSize, Qt.SolidLine,
                        Qt.RoundCap, Qt.RoundJoin)
        imageName = color + ".png"
        imageName = imageName.replace(' ', '')
        path = util.join(penPath, imageName) 
        self.cursorPixmap = path
        self.setPenSize(self.penSize)
    
    def setPenSize(self, size):
        self.penSize = size
        self.pen = QPen(self.penColor, self.penSize, Qt.SolidLine,
                        Qt.RoundCap, Qt.RoundJoin)
        size = int(round(size*4.2 + 12))
        pix = QPixmap(self.cursorPixmap)
        pix = pix.scaled(size, size, Qt.KeepAspectRatio,
                         Qt.SmoothTransformation)
        self.setCursor(QCursor(pix, 0, size))
        
    def undo(self):
        pass

    def saveImage(self):
        self.pix.save('D:/My/test/hello.png', None, 100)
    
    def isModified(self):
        return self.modified
    
    def clearImage(self):
        
        self.modified = True
            
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self.pix)
        
    def wheelEvent(self, event):
        delta = event.delta()
        penSize = self.penSize
        if delta < 0:
            if penSize > 1:
                self.setPenSize(penSize - 1)
        if delta > 0:
            if penSize < 20:
                self.setPenSize(penSize + 1)
        # hack to handle the display bug of not resizing the cursor
        self.cursor().setPos(self.cursor().pos())
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.mouseDown = True
            self.end = self.start = event.pos()
            self.paint()
        
    def mouseMoveEvent(self, event):
        if self.mouseDown:
            self.end = event.pos()
            self.paint()
            self.start = event.pos()
        
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.mouseDown = False
        if event.button() == Qt.RightButton:
            self.menu = Menu(self.parentWin)
            self.menu.popup(QCursor.pos())
        
    def paint(self):
        painter = QPainter(self.pix)
        painter.setPen(self.pen)
        if self.start == self.end:
            painter.drawPoint(self.start)
        else:
            painter.drawLine(self.start, self.end)
        painter.end()
        self.update()
            
Form, Base = uic.loadUiType('%s\ui\preferences.ui'%root)
class Preferences(Form, Base):
    
    def __init__(self, parentWin = None):
        super(Preferences, self).__init__(parentWin)
        self.setupUi(self)
            
class Menu(QMenu):
    
    def __init__(self, parentWin = None):
        super(Menu, self).__init__(parentWin)
        self.parentWin = parentWin
        self.setActions()
    
    def setActions(self):
        # create main actions
        penColorAct = QAction('Pen Color', self)
        self.addAction(penColorAct)
        moreActs = ['Preferences', 'Help', 'Cancel']
        # connect main actions to functions
        acts = self.actions()
        map(lambda act: act.triggered.connect(lambda: self.handleActs(act)),
            acts)
        # create menu for pen color action
        menu = QMenu(self)
        colorActs = ['White', 'Black', 'Red', 'Dark Red', 'Green',
                     'Dark Green','Blue', 'Dark Blue', 'Cyan', 'Dark Cyan',
                     'Yellow', 'Dark Yellow']
        # add color actions to pen color menu
        for act in colorActs:
            menu.addAction(QAction(act, self))
        penColorAct.setMenu(menu)
        colorActions = menu.actions()
        # connect pen color actions to function
        map(lambda act: act.triggered.connect
            (lambda: self.handleColorActs(act)), colorActions)
        
    def handleColorActs(self, act):
        text = str(act.text())
        self.parentWin.paintArea.setPenColor(text)
        
    def handleActs(self, act):
        text = act.text()
        
        
        
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