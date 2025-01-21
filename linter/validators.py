import re
from enum import Enum
from maya import cmds

class ValidationError:
    def __init__(self, elType, file, elName, issue):
        self.file = file
        self.elType = elType
        self.elName = elName
        self.issue = issue
    
    def __str__(self):
        return (self.file + ": " + self.elName + " - " + self.issue)
        
    def __repr__(self):
        return (self.file + ": " + self.elName + " - " + self.issue)

class ElementType(Enum):
    FILE = 1
    NODE = 2
    CONFIG = 3

def nodeGeometryNaming(file, meshNode):
    transform = cmds.listRelatives(meshNode, parent=True)[0]
    if not re.search(r'.*_(SCULPT)?(GEO|PRXY)(_LOW|_HIGH)?(\d)*$', transform):
        return ValidationError(ElementType.NODE, file, transform, "Geometry incorrectly named")

def nodeCtrlNaming(file, ctrlNode):
    transform = cmds.listRelatives(ctrlNode, parent=True)[0]
    if not re.search(r'.*(_L)?(_R)?_?.*_(CTRL|CRV)$', transform):
        return ValidationError(ElementType.NODE, file, transform, "Control incorrectly named")

def nodeJointNaming(file, jointNode):
    if not re.search(r'.*(_L)?(_R)?_.*_JNT$', jointNode):
        return ValidationError(ElementType.NODE, file, jointNode, "Joint incorrectly named")

def nodeCameraNaming(file, cameraNode):
    transform = cmds.listRelatives(cameraNode, parent=True)[0]
    if not re.search(r'(persp|top|front|side|bottom|sh\d\d\d\d_shotCam.*)', transform):
        return ValidationError(ElementType.NODE, file, transform, "Camera incorrectly named")

def referencePrefixNaming(file, referenceNode):
    if (re.search(r'.*sharedReferenceNode.*',referenceNode) or referenceNode == "_UNKNOWN_REF_NODE_"):
        return
    try:
        namespace = cmds.referenceQuery(referenceNode, namespace=True)
        if not re.search(r'(:env|:rigA|:rigG|:rigL)', namespace):
            return ValidationError(ElementType.NODE, file, namespace, "Reference incorrectly namespaced")
    except RuntimeError:
        return ValidationError(ElementType.NODE, file, referenceNode, "Reference crash!")

def referenceFilePath(file, referenceNode):
    if (re.search(r'.*sharedReferenceNode.*',referenceNode) or referenceNode == "_UNKNOWN_REF_NODE_"):
        return
    try:
        filename = cmds.referenceQuery(referenceNode, filename=True)
        if not re.search(r'^P:', filename):
            return ValidationError(ElementType.NODE, file, filename, "Reference not on P Drive")
    except RuntimeError:
        return ValidationError(ElementType.NODE, file, referenceNode, "Reference crash!")

def nodeMaterialNaming(file, materialNode):
    if not re.search(r'.*_?.*_(TEX|MAT)$', materialNode):
        return ValidationError(ElementType.NODE, file, materialNode, "Material incorrectly named")

def mtoaIsDisabled(file):
    if cmds.pluginInfo("mtoa", query=True, loaded=True):
        return ValidationError(ElementType.FILE, file, '', "Arnold Plugin is loaded")

def fileNaming(file):
    if(re.search(r'.*sh\d\d\d\d.*', file)): #shot pipeline
        if not re.search(r'.*AWA_sh\d\d\d\d_(STB|LYT|ANIM|FX|LGT|CMP)_v\d\d\d_[A-Z]{2}[A-Z]?', file):
            return ValidationError(ElementType.FILE, file, '', "File name does not follow Shot Pipeline naming conventions")
    else: #asset pipeline
        if not re.search(r'.*AWA_[A-Za-z]*_(PRXY|MDL|SRF|SCLP|CSCLP|SPT|RIG)_(v\d\d\d_[A-Z]{2}[A-Z]?|MASTER)', file):
            return ValidationError(ElementType.FILE, file, '', "File name does not follow Asset Pipeline naming conventions")


def fileNoNoArnolds(file):
    if(re.search(r'.*noArnold.*', file)): 
        return ValidationError(ElementType.FILE, file, '', "File has a '-noArnold' extension")

#    elif re.search(r'Pxr.*Light', nodeType ) and not re.search(r'.*_.*_pxr.*Light(\d)*$', transform):
#        print("X " + transform + " (" + nodeType + ") does not meet light naming convention.")