"""
Maya/QT UI template
Maya 2023
https://gist.github.com/isaacoster
"""

import maya.cmds as cmds
import os
from maya import OpenMayaUI as omui
from shiboken2 import wrapInstance
from PySide2 import QtUiTools, QtCore, QtGui, QtWidgets
from functools import partial # optional, for passing args during signal function calls
import sys

class ResultUI(QtWidgets.QWidget):

    window = None
    data = None
    
    def __init__(self, parent = None):
        super(ResultUI, self).__init__(parent = parent)
        self.setWindowFlags(QtCore.Qt.Window)
        self.widgetPath = (os.path.dirname(__file__))
        self.widget = QtUiTools.QUiLoader().load(self.widgetPath + '/result_UI.ui')
        self.widget.setParent(self)
        # set initial window size
        self.resize(300, 800)      
        # locate UI widgets
        self.btn_scan = self.widget.findChild(QtWidgets.QPushButton, 'btn_scan')      
        self.tree_scanResults = self.widget.findChild(QtWidgets.QTreeWidget, 'tree_scanResults')  
        


        self.tree_scanResults.setColumnCount(2)

        for item in ResultUI.data :
            myWidget = QtWidgets.QTreeWidgetItem([item.elName,item.issue])
            self.tree_scanResults.addTopLevelItem(myWidget)

        self.tree_scanResults.itemClicked.connect(self.onItemClicked)



        # assign functionality to buttons
        self.btn_scan.clicked.connect(self.scan)
    
    def scan(self):
        print ("Scan")

    def onItemClicked(self):
        item = self.tree_scanResults.currentItem()
        print (item.text(0))
        cmds.select(item.text(0))

    def resizeEvent(self, event):
        self.widget.resize(self.width(), self.height())
        
    def closeWindow(self):
        print ('closing window')
        self.destroy()
    
    def setData(data):
        ResultUI.data = data
    
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

