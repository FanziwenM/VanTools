import sys
import maya.api.OpenMaya as om


def maya_useNewAPI():
    """
    The presence of this function tells Maya that the plugin produces, and
    expects to be passed, objects created using the Maya Python API 2.0.
    """
    pass


# command
class PyHelloWorldCmd(om.MPxCommand):
    kPluginCmdName = "pyHelloWorld"

    def __init__(self):
        om.MPxCommand.__init__(self)

    @staticmethod
    def cmdCreator():
        return PyHelloWorldCmd()

    def doIt(self, args):
        print "Hello World!"


class newCmd(om.MPxCommand):
    kPluginCmdName = "myPrintTime"

    def __init__(self):
        om.MPxCommand.__init__(self)

    @staticmethod
    def cmdCreator():
        return newCmd()

    def doIt(self, *args):
        import time
        print(time.localtime(time.time()))


# Initialize the plug-in
def initializePlugin(plugin):
    pluginFn = om.MFnPlugin(plugin)
    try:
        pluginFn.registerCommand(
            PyHelloWorldCmd.kPluginCmdName, PyHelloWorldCmd.cmdCreator
        )
        pluginFn.registerCommand(
            newCmd.kPluginCmdName, newCmd.cmdCreator
        )
    except Exception:
        sys.stderr.write(
            "Failed to register command: %s\n" % PyHelloWorldCmd.kPluginCmdName
        )
        raise


# Uninitialize the plug-in
def uninitializePlugin(plugin):
    pluginFn = om.MFnPlugin(plugin)
    try:
        pluginFn.deregisterCommand(PyHelloWorldCmd.kPluginCmdName)
    except:
        sys.stderr.write(
            "Failed to unregister command: %s\n" % PyHelloWorldCmd.kPluginCmdName
        )
        raise
