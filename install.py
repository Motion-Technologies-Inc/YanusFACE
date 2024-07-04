# Libraries
import os

import maya.cmds as cmds
import maya.mel


def onMayaDroppedPythonFile(*args, **kwargs):
    # Maya info
    mayaVersion = cmds.about(version=True)
    mainShelf = 'YanusStudio'
    buttonLabel = 'YanusFACE'

    # Init paths
    currentDir = os.path.dirname(__file__)
    scriptPath = os.path.join(
        currentDir,
        'scripts',
        'development' if os.path.exists(os.path.join(currentDir, 'scripts', 'development')) else mayaVersion)
    icon_file_name = "YanusFaceFA.png"
    icon_path = os.path.join(currentDir, 'icons', icon_file_name)

    # Maya command
    gShelfTopLevel = maya.mel.eval("$gShelfTopLeveltmpVar=$gShelfTopLevel")

    # Create new shelf tab named 'YanusStudio' if it doesn't exist
    if not cmds.shelfLayout(mainShelf, exists=True):
        cmds.shelfLayout(mainShelf, parent=gShelfTopLevel)

    # Check for existing button and delete if found
    shelf_buttons = cmds.shelfLayout(mainShelf, query=True, childArray=True) or []
    for button in shelf_buttons:
        if cmds.shelfButton(button, query=True, label=True) == buttonLabel:
            cmds.deleteUI(button)

    # Setup for Mayas versions
    command = """from importlib import reload
import sys

# Init path in system
scripts_path = r"{scripts_path}"
if scripts_path not in sys.path:
    sys.path.append(scripts_path)
        
# Import main class
import YFmain

# Reload modules
reload(YFmain)

# Run main class
yanusFACE = YFmain.YanusFACE()
""".format(scripts_path=scriptPath)

    # Run Maya command
    cmds.shelfButton(image1=icon_path, p=mainShelf, rpt=True, c=command, label=buttonLabel)
