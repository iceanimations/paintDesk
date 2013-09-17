'''
Created on Sep 12, 2013

@author: qurban.ali
'''
import site
site.addsitedir(r"R:/Python_Scripts")
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import secondary as sec
from .logic import utilities as util
prefFile = util.prefFile()
modulePath = util.modulePath(__name__)
root = util.dirname(util.dirname(util.dirname(modulePath)))

class Window(QWidget):
    def __init__(self, parent = None):
        super(Window, self).__init__(parent)
        layout = QStackedLayout()
        self.paintArea = sec.PaintArea(self)
        layout.addWidget(self.paintArea)
        self.setLayout(layout)
        self.fileName = ''
        self.imgQuality = 50
        self.setWindowTitle('paintDesk')
        self.setWindowIcon(QIcon('%s\icons\pd.png'%root))
        self.setWindowFlags(Qt.MSWindowsFixedSizeDialogHint)
        self.setWindowFlags(Qt.CustomizeWindowHint)
        self.setWindowFlags(Qt.FramelessWindowHint)
        # show preferences dialog
        self.setPreferences()
        
    def setPreferences(self):
        fd = open(prefFile)
        data = fd.read()
        fd.close()
        if not data:
            win = sec.Preferences(self)
            win.show()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.closeWin()
        if event.key() == Qt.Key_S:
            self.paintArea.saveImage()
            
    def openFile(self):
        if self.paintArea.modified:
            btn = sec.msgBox(self, msg = 'File has been modified',
                       ques = 'Do you want to save the changes?',
                       icon = QMessageBox.Information,
                       btns=QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            if btn == QMessageBox.Yes:
                self.saveFile()
            elif btn == QMessageBox.No:
                pass
            else: return
        path = sec.openFileDialog(self)
        if path:
            self.paintArea.pix = QPixmap(path)
            self.fileName = path
            self.paintArea.update()
    
    def saveImage(self):
        if self.paintArea.pix.save(self.fileName,None,self.imgQuality):
            self.paintArea.modified = False
            return True
        else: return False
            
    def saveFile(self):
        if self.fileName:
            if not self.saveImage():
                sec.msgBox(self, msg = 'File not saveed, check preferences'+
                           ' or path that you specified',
                           icon = QMessageBox.Information)
                return False
            self.paintArea.modified = False
            return True
        else:
            return self.saveNewFile()

    def saveNewFile(self):
        fd = open(prefFile)
        data = fd.read()
        if not data:
            win = sec.Preferences(self)
            win.exec_()
            fd.seek(0)
            data = fd.read()
            fd.close()
            if not data: return
        prefs = eval(data)
        if prefs['alwaysAsk']:
            return self.saveAsFile()
        elif prefs['alwaysSave']:
            path = prefs['path']
            if not path or not util.exists(path):
                sec.msgBox(self, msg = 'The system can not find the path '+
                           'specified, check your preferences',
                           icon = QMessageBox.Information)
                return False
            fileName = prefs['fileName']
            if not fileName:
                sec.msgBox(self, msg = 'File name not found, check your '+
                           'Preferences', icon = QMessageBox.Information)
                return False
            uniqueNum = util.nextFileName(path)
            uniqueFileName = fileName + str(uniqueNum)
            if uniqueFileName:
                self.fileName = util.join(path, uniqueFileName + '.png')
                self.saveImage()
                return True

    def saveAsFile(self):
        path = sec.saveFileDialog(self)
        if path:
            path = util.splitext(path)[0]
            self.fileName = path + '.png'
            self.saveImage()
            return True
        else: return False

    def clearImage(self):
        if self.paintArea.modified:
            btn = sec.msgBox(self, msg = 'Unsaved changes in the file',
                       ques = 'Do you want to save the changes?',
                       icon = QMessageBox.Information,
                       btns=QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            if btn == QMessageBox.Yes:
                self.saveFile()
            if btn == QMessageBox.No:
                pass
            if btn == QMessageBox.Cancel:
                return
        self.paintArea.pix.fill(QColor(0,0,0, alpha = 0))
        self.paintArea.modified = True
        self.fileName = ''
    
    def showHelp(self):
        sec.msgBox(self, msg = util.helpText, title = 'Help',
                   icon = QMessageBox.Information)
    
    def closeWin(self):
        if self.paintArea.modified:
            btn = sec.msgBox(self, msg = 'Unsaved changes in the file',
                       ques = 'Do you want to save the changes?',
                       icon = QMessageBox.Information,
                       btns=QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            if btn == QMessageBox.Yes:
                if not self.saveFile():
                    return
            if btn == QMessageBox.No:
                pass
            if btn == QMessageBox.Cancel:
                return
        self.close()
    