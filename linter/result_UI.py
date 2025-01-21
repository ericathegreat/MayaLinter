"""
Maya/QT UI template
Maya 2023
https://gist.github.com/isaacoster
"""

import maya.cmds as cmds
import maya.mel as mel
import os
from maya import OpenMayaUI as omui
from shiboken2 import wrapInstance
from PySide2 import QtUiTools, QtCore, QtGui, QtWidgets
from functools import partial # optional, for passing args during signal function calls
import sys

class ResultUI(QtWidgets.QWidget):

    window = None
    
    def __init__(self, parent = None):
        super(ResultUI, self).__init__(parent = parent)
        self.setWindowFlags(QtCore.Qt.Window)
        self.widgetPath = (os.path.dirname(__file__))
        print(self.widgetPath)
        self.widget = QtUiTools.QUiLoader().load(self.widgetPath + '/result_UI.ui')
        self.widget.setParent(self)
        # set initial window size
        self.resize(300, 800)      
        # locate UI widgets
        self.btn_scan = self.widget.findChild(QtWidgets.QPushButton, 'btn_scan')                 
        # assign functionality to buttons
        self.btn_scan.clicked.connect(self.scan)
        #self.linterCore = MayaLinterCore()
    
    
    def scan(self):
        print ("Hello World")

    def resizeEvent(self, event):
        self.widget.resize(self.width(), self.height())
        
    def closeWindow(self):
        print ('closing window')
        self.destroy()
    
    def openWindow():
        # Maya uses this so it should always return True
        if QtWidgets.QApplication.instance():
            # Id any current instances of tool and destroy
            for win in (QtWidgets.QApplication.allWindows()):
                if 'ResultUI' in win.objectName(): # update this name to match name below
                    win.destroy()

        mayaMainWindowPtr = omui.MQtUtil.mainWindow()
        mayaMainWindow = wrapInstance(int(mayaMainWindowPtr), QtWidgets.QWidget)
        ResultUI.window = ResultUI(parent = mayaMainWindow)
        ResultUI.window.setObjectName('ResultUI') # code above uses this to ID any existing windows
        ResultUI.window.setWindowTitle('Maya Linter UI')
        ResultUI.window.show()
