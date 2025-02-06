# -*- coding: utf-8 -*-

import maya.api.OpenMaya as om
import sys
from linter import MayaLinterCmd

def maya_useNewAPI():
    """
    The presence of this function tells Maya that the plugin produces, and
    expects to be passed, objects created using the Maya Python API 2.0.
    """
    pass

def initializePlugin( obj ):
    plugin = om.MFnPlugin(obj)
    try:
        plugin.registerCommand( MayaLinterCmd.name, MayaLinterCmd.cmdCreator, MayaLinterCmd.createSyntax) 
        print ("Registered")
    except:
        sys.stderr.write(
            "Failed to register command: %s\n" % MayaLinterCmd.name
        )


# Uninitialize the plug-in
def uninitializePlugin(plugin):
    pluginFn = om.MFnPlugin(plugin)
    try:
        pluginFn.deregisterCommand(MayaLinterCmd.name)
        print ("Deregistered")
    except:
        sys.stderr.write(
            "Failed to unregister command: %s\n" % MayaLinterCmd.name
        )