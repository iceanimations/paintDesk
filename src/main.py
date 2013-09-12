'''
Created on Sep 12, 2013

@author: qurban.ali
'''
import site
site.addsitedir(r"R:/Python_Scripts")
from PyQt4.QtGui import QApplication
import sys
import interface.window as window

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = window.Window()
    win.showMaximized()
    sys.exit(app.exec_())