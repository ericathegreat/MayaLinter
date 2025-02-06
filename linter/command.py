
import maya.api.OpenMaya as om
from linter.result_UI import ResultUI
import linter.validators as validators
import maya.cmds as cmds
import re

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
        syntax.addFlag("-ui", "-showUI", om.MSyntax.kBoolean)
        return syntax

    def doIt(self, args):
        argData = om.MArgDatabase(self.syntax(), args)
        validationErrors = self.processFile()

        if (argData.isFlagSet("-ui") and argData.flagArgumentBool("-ui",0)):
            ResultUI.setData(validationErrors)
            ResultUI.openWindow()

        self.setResult(self.errorsToStringArray(validationErrors))

    node_validators = {
        "mesh": [validators.nodeGeometryNaming],
        "nurbsCurve": [validators.nodeCtrlNaming],
        "joint": [validators.nodeJointNaming],
        "camera" : [validators.nodeCameraNaming],
        "reference": [validators.referenceFilePath], #validators.referencePrefixNaming, 
        #"PxrSurface": [validators.nodeMaterialNaming]
    }

    def processFile(self):
        validationErrors = []
        for nodeType in self.node_validators:
            for node in cmds.ls(type=nodeType):
                if(re.search(r':',node)): # Don't include referenced nodes
                    continue
                for validator in self.node_validators[nodeType]:
                    result = validator(node)
                    if not result is None:
                        validationErrors.append(result)
        return validationErrors
    
    def errorsToStringArray(self, errorList):
        result = []
        for error in errorList:
            result.append (error.elName + ": " + error.issue)
        return result