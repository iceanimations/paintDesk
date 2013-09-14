'''
Created on Sep 12, 2013

@author: qurban.ali
'''
import os
osp = os.path
import sys

def modulePath(name):
    '''returns the path to the module "name"'''
    return sys.modules[name].__file__

def dirname(path):
    return osp.dirname(path)

def join(path1, path2):
    return osp.join(path1, path2)