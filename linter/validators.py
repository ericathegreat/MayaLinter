import re
from enum import Enum
from maya import cmds

class ValidationError:
    def __init__(self, elType, elName, issue, notes = ""):
        self.elType = elType
        self.elName = elName
        self.issue = issue
        self.notes = notes
    
    def __str__(self):
        return (self.elName + " - " + self.issue)
        
    def __repr__(self):
        return (self.elName + " - " + self.issue)

class ElementType(Enum):
    FILE = 1
    NODE = 2
    CONFIG = 3

def nodeGeometryNaming(meshNode):
    transform = cmds.listRelatives(meshNode, parent=True)[0]
    if not re.search(r'.*_(SCULPT)?(GEO|PRXY)(_LOW|_HIGH)?(\d)*$', transform):
        return ValidationError(ElementType.NODE, transform, "Geometry incorrectly named")

def nodeCtrlNaming(ctrlNode):
    transform = cmds.listRelatives(ctrlNode, parent=True)[0]
    if not re.search(r'.*(_L)?(_R)?_?.*_(CTRL|CRV)$', transform):
        return ValidationError(ElementType.NODE, transform, "Control incorrectly named")

def nodeJointNaming(jointNode):
    if not re.search(r'.*(_L)?(_R)?_.*_JNT$', jointNode):
        return ValidationError(ElementType.NODE, jointNode, "Joint incorrectly named")

def nodeCameraNaming(cameraNode):
    transform = cmds.listRelatives(cameraNode, parent=True)[0]
    if not re.search(r'(persp|top|front|side|bottom|sh\d\d\d\d_shotCam.*)', transform):
        return ValidationError(ElementType.NODE, transform, "Camera incorrectly named")

def referencePrefixNaming(referenceNode):
    if (re.search(r'.*sharedReferenceNode.*',referenceNode) or referenceNode == "_UNKNOWN_REF_NODE_"):
        return
    try:
        namespace = cmds.referenceQuery(referenceNode, namespace=True)
        if not re.search(r'(:env|:rigA|:rigG|:rigL)', namespace):
            return ValidationError(ElementType.NODE, namespace, "Reference incorrectly namespaced")
    except RuntimeError:
        return ValidationError(ElementType.NODE, referenceNode, "Reference crash!")

def referenceFilePath(referenceNode):
    if (re.search(r'.*sharedReferenceNode.*',referenceNode) or referenceNode == "_UNKNOWN_REF_NODE_"):
        return
    try:
        filename = cmds.referenceQuery(referenceNode, filename=True)
        if not re.search(r'^P:', filename):
            return ValidationError(ElementType.NODE, filename, "Reference not on P Drive")
    except RuntimeError:
        return ValidationError(ElementType.NODE, referenceNode, "Reference crash!")

def nodeMaterialNaming(materialNode):
    if not re.search(r'.*_?.*_(TEX|MAT)$', materialNode):
        return ValidationError(ElementType.NODE, materialNode, "Material incorrectly named")

def mtoaIsDisabled():
    if cmds.pluginInfo("mtoa", query=True, loaded=True):
        return ValidationError(ElementType.FILE, '', "Arnold Plugin is loaded")
