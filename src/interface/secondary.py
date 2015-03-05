'''
Created on Sep 12, 2013

@author: qurban.ali
'''
import site
site.addsitedir(r"R:/Python_Scripts")
site.addsitedir(r"R:\Pipe_Repo\Users\Hussain\packages\iutilities")
import iutilities as utl
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import uic
from .logic import utilities as util
modulePath = util.modulePath(__name__)
root = util.dirname(util.dirname(util.dirname(modulePath)))
penPath = r"%s\icons\pen"%root
prefFile = util.prefFile()

class PaintArea(QLabel):
    def __init__(self, parentWin = None):
        super(PaintArea, self).__init__(parentWin)
        self.parentWin = parentWin
        self.modified = False
        self.image = QImage()
        self.mouseDown = False
        self.points = []
        self.eraser = False
        self.backPix = QPixmap.grabWindow(QApplication.desktop().winId())
        imagePath = util.tempPath()
        self.backPix.save(imagePath, None, 100)
        self.setStyleSheet("background-image: url(%s)"%imagePath)
        self.pix = QPixmap(self.backPix.size())
        self.pix.fill(QColor(0,0,0, alpha = 0))
        
        self.colors = {'White': Qt.white, 'Black': Qt.black, 'Red': Qt.red,
              'Dark Red': Qt.darkRed, 'Green': Qt.green,
              'Dark Green': Qt.darkGreen, 'Blue': Qt.blue,
              'Dark Blue': Qt.darkBlue, 'Cyan': Qt.cyan,
              'Dark Cyan': Qt.darkCyan, 'Magenta': Qt.magenta,
              'Dark Magenta': Qt.darkMagenta, 'Yellow': Qt.yellow,
              'Dark Yellow': Qt.darkYellow}
        self.penSize = 3
        self.eraserSize = 2
        self.setPenColor('Black')
        self.start = self.end = None

    def setPenColor(self, color):
        self.penColor = self.colors[color]
        self.pen = QPen(self.penColor, self.penSize, Qt.SolidLine,
                        Qt.RoundCap, Qt.RoundJoin)
        path = util.penPixPath(penPath, color) 
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
        self.eraser = False
        self.cursor().setPos(QCursor.pos())
        
    def setEraserSize(self, size):
        self.eraserSize = size
        path = r"%s\icons\eraser\eraser"%root
        path = path + str(size*16) + ".png"
        self.setCursor(QCursor(QPixmap(path), 0,0))
        self.cursor().setPos(QCursor.pos())
            
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self.pix)
        
    def wheelEvent(self, event):
        delta = event.delta()
        if not self.eraser:
            self.changePenSize(delta)
        else:
            self.changeEraserSize(delta)
        # hack to handle the display bug of not resizing the cursor
        self.cursor().setPos(self.cursor().pos())
    
    def changePenSize(self, delta):
        penSize = self.penSize
        if delta < 0:
            if penSize > 1:
                self.setPenSize(penSize - 1)
        if delta > 0:
            if penSize < 20:
                self.setPenSize(penSize + 1)
        self.eraser = False
                
    def changeEraserSize(self, delta):
        size = self.eraserSize
        if delta < 0:
            if size > 1:
                self.setEraserSize(size - 1)
        if delta > 0:
            if size < 6:
                self.setEraserSize(size + 1)
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.mouseDown = True
            self.end = self.start = event.pos()
            self.pushUndoCommand(UndoCommand(self.pix, self))
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
            self.parentWin.menu.popup(QCursor.pos())
        
    def paint(self):
        painter = QPainter(self.pix)
        painter.setPen(self.pen)
        if self.start == self.end:
            if self.eraser:
                self.erase(painter)
            else:
                painter.drawPoint(self.start)
        else:
            if self.eraser:
                self.erase(painter)
            else:
                painter.drawLine(self.start, self.end)
        painter.end()
        self.update()
        self.modified = True
        
    def erase(self, painter):
        rect = QRect(self.cursor().pos(), self.cursor().pixmap().size())
        cpix = self.backPix.copy(rect)
        painter.drawPixmap(rect.topLeft(), cpix)
        
    def pushUndoCommand(self, command):
        if command:
            self.parentWin.undoStack.push(command)
            
Form, Base = uic.loadUiType('%s\ui\preferences.ui'%root)
class Preferences(Form, Base):
    
    def __init__(self, parentWin = None):
        super(Preferences, self).__init__(parentWin)
        self.setupUi(self)
        self.parentWin = parentWin
        self.alwaysAskButton.clicked.connect(self.switchPathBox)
        self.alwaysSaveButton.clicked.connect(self.switchPathBox)
        self.browseButton.clicked.connect(self.setPathBoxText)
        self.saveButton.clicked.connect(self.save)
        self.cancelButton.clicked.connect(self.close)
        regex = QRegExp('\\w+')
        validator = QRegExpValidator(regex, self)
        self.fileNameBox.setValidator(validator)
        self.loadPreferences()
        
    def loadPreferences(self):
        fd = open(prefFile)
        data = fd.read()
        if not data: return
        prefs = eval(data)
        if prefs['alwaysAsk']:
            return
        self.alwaysSaveButton.setChecked(True)
        if prefs['path']:
            self.pathBox.setText(prefs['path'])
            self.pathBox.setEnabled(True)
            self.browseButton.setEnabled(True)
        if prefs['fileName']:
            self.fileNameBox.setText(prefs['fileName'])
            self.fileNameBox.setEnabled(True)
        
    def switchPathBox(self):
        flag = self.alwaysSaveButton.isChecked()
        self.pathBox.setEnabled(flag)
        self.browseButton.setEnabled(flag)
        self.fileNameBox.setEnabled(flag)
        if not flag:
            self.pathBox.clear()
            self.fileNameBox.clear()
        
    def setPathBoxText(self):
        path = folderDialog(self.parentWin)
        if path:
            self.pathBox.setText(path)
        
    def save(self):
        alwaysAsk = self.alwaysAskButton.isChecked()
        alwaysSave = self.alwaysSaveButton.isChecked()
        path = None
        fileName = None
        if alwaysSave:
            path = str(self.pathBox.text())
            if not path or not util.exists(path):
                msgBox(self.parentWin,
                       msg = 'The system can not find the path specified',
                       icon = QMessageBox.Information)
                return
            fileName = str(self.fileNameBox.text())
            if not fileName:
                msgBox(self.parentWin, msg = 'File name must be spedified in'+
                       ' order to save the file',
                       icon = QMessageBox.Information)
                return
        pref = {'alwaysAsk': alwaysAsk, 'alwaysSave': alwaysSave,
                'path': path, 'fileName': fileName}
        fd = open(prefFile, 'w')
        fd.write(str(pref))
        fd.close()
        self.close()
        
            
class Menu(QMenu):
    
    def __init__(self, parentWin = None):
        super(Menu, self).__init__(parentWin)
        self.parentWin = parentWin
        self.setActions()
    
    def setActions(self):
        # create main actions
        penColorAct = QAction('Pen Color', self.parentWin)
        penColorAct.setShortcutContext(Qt.ApplicationShortcut)
        self.addAction(penColorAct)
        eraserAct = QAction('Eraser', self.parentWin)
        self.addAction(eraserAct)
        eraserAct.setShortcut(QKeySequence(Qt.Key_E))
        self.addSeparator()
        moreActs = ['New', 'Open', 'Save', 'Save As...', 'Preferences',
                    'Help', 'Clear', 'Exit']
        for act in moreActs:
            actObj = QAction(act, self.parentWin)
            self.addAction(actObj)
            if act == 'Preferences':
                actObj.setShortcut(QKeySequence(Qt.CTRL + Qt.SHIFT + Qt.Key_P))
            if act == 'Save As...':
                self.addSeparator()
            if act == 'New':
                actObj.setShortcut(QKeySequence(QKeySequence(QKeySequence.New)))
            if act == 'Open':
                actObj.setShortcut(QKeySequence(QKeySequence.Open))
            if act == 'Save':
                actObj.setShortcut(QKeySequence(QKeySequence.Save))
            if act == 'Help':
                actObj.setShortcut(QKeySequence(QKeySequence.HelpContents))
                self.addSeparator()
                undoAction = self.parentWin.undoStack.createUndoAction(self.parentWin, 'Undo')
                self.addAction(undoAction)
                undoAction.setShortcut(QKeySequence(QKeySequence.Undo))
                redoAction = self.parentWin.undoStack.createRedoAction(self.parentWin, 'Redo')
                redoAction.setShortcut(QKeySequence(QKeySequence.Redo))
                self.addAction(redoAction)
                self.addSeparator()
            if act == 'Clear':
                actObj.setShortcut(QKeySequence(QKeySequence.Delete))
            if act == 'Exit':
                actObj.setShortcut(QKeySequence(Qt.Key_Escape))
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
        for name in colorActs:
            act = QAction(name, self)
            menu.addAction(act)
            act.setIcon(QIcon(self.colorIcon(name)))
        penColorAct.setMenu(menu)
        colorActions = menu.actions()
        # connect pen color actions to function
        map(lambda act: act.triggered.connect
            (lambda: self.handleColorActs(act)), colorActions)
        
    def colorIcon(self, name):
        return util.penPixPath(penPath, name)
        
    def handleColorActs(self, act):
        text = str(act.text())
        self.parentWin.paintArea.setPenColor(text)
        
    def handleActs(self, act):
        text = act.text()
        if text == 'Preferences':
            win = Preferences(self.parentWin)
            win.show()
        if text == 'Eraser':
            self.parentWin.paintArea.setEraserSize(self.parentWin.paintArea.eraserSize)
            self.parentWin.paintArea.eraser = True
        if text == 'New':
            self.parentWin.createNew()
            self.parentWin.fileName = ''
        if text == 'Open':
            self.parentWin.openFile()
        if text == 'Save':
            self.parentWin.saveFile()
        if text == 'Save As...':
            self.parentWin.saveAsFile()
        if text == 'Clear':
            self.parentWin.createNew()
        if text == 'Help':
            self.parentWin.showHelp()
        if text == 'Exit':
            self.parentWin.closeWin()
        
class UndoCommand(QUndoCommand):
    def __init__(self, img, paintArea, parent = None):
        super(UndoCommand, self).__init__(parent)
        self.prevPix = QPixmap(img)
        self.currentPix = QPixmap(self.prevPix)
        self.paintArea = paintArea
        
    def undo(self):
        self.currentPix = QPixmap(self.paintArea.pix)
        self.paintArea.pix = self.prevPix
        self.paintArea.update()
    
    def redo(self):
        self.paintArea.pix = self.currentPix
        self.paintArea.update()
    
        
        
def saveFileDialog(parent = None):
    fileName = QFileDialog.getSaveFileName(parent, 'Save file', '', '*.png')
    if fileName: return str(fileName)
    else: return None

def openFileDialog(parent):
    fileName = QFileDialog.getOpenFileName(parent, 'Open Image', '', '*.png')
    if fileName: return str(fileName)
    else: return None
    
def folderDialog(parent):
    name = QFileDialog.getExistingDirectory(parent, 'Select Directory', '',
                                     QFileDialog.ShowDirsOnly)
    if name: return str(name)
    else: return None
        
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