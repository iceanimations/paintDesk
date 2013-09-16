'''
Created on Sep 12, 2013

@author: qurban.ali
'''
import os
osp = os.path
import sys
from PyQt4.QtCore import *

def modulePath(name):
    '''returns the path to the module "name"'''
    return sys.modules[name].__file__

def dirname(path):
    return osp.dirname(path)

def join(path1, path2):
    return osp.join(path1, path2)

def exists(path):
    return osp.exists(path)

def penPixPath(penPath, color):
    imageName = color + ".png"
    imageName = imageName.replace(' ', '')
    return join(penPath, imageName)

def userHomeDir():
    return osp.expanduser('~')

def homeDir():
    return join(userHomeDir(), '.paintDesk')

def prefFile():
    return join(homeDir(), 'pref.txt')

def createHomeDir():
    try:
        os.mkdir(homeDir())
    except: pass
    
def splitext(path):
    return osp.splitext(path)

def createPrefFile():
    try:
        if not osp.exists(prefFile()):
            fd = open(prefFile(), 'w')
            fd.close()
    except: pass
    
def nextFileName(directory = ''):
    if directory:
        files = os.listdir(directory)
        count = len(files)
        regex = QRegExp('(\\d+)')
        greater = 0
        for f in files:
            index = regex.indexIn(f)
            if index > -1:
                num = int(regex.cap(1))
                if num > greater: greater = num
        return greater + 1
    else: return None
    
helpText = ('<b>paintDesk</b> makes it easy to create notes for your current'+
            ' desktop screenshot by facilitating you to paint your screenshot'+
            ' with different colors and pen sizes.<br><br>'+
            '<b>How to use:</b> click and drag on the screenshot to paint'+
            '.<br><b>Pen Size:</b> Scroll up and down to change the size of'+
            'pen.<br><b>Erase:</b> press "e" on you keyboard to change the'+
            ' cursor to eraser tool and "p" to set get back the pen tool.<br>'+
            '<b>Undo:</b> Ctrl+Z<br>'
            '<b>context Menu:</b> Right click on any part of screenshot to'+
            ' access the wide range of options (including pen color and '+
            'preferences.)')
                
        
    