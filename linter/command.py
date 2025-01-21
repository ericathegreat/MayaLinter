
import maya.api.OpenMaya as om
from linter.result_UI import ResultUI

class MayaLinterCmd(om.MPxCommand):
    name = "linter"

    def __init__(self):
        om.MPxCommand.__init__(self)

    @staticmethod
    def cmdCreator():
        return MayaLinterCmd()
    
    @staticmethod
    def createSyntax():
        """Creates the MEL syntax"""
        syntax = om.MSyntax()
        return syntax

    def doIt(self, args):
        print(args)
        ResultUI.openWindow()