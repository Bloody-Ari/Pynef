#########################################################
#                   Quick Example                       #
#########################################################
# openDefaultFile()                                     #
# updateNozzle(12.75/2, 3.370, 6.010/2, 3.6, 7.940/2)   #
# exportNozzle("NewNozzle", "stl")                      #
#                                                       #
# Why 12.75/2? updateNozzle uses radius, so if you have #
# the diameter (way easier to measure), you just divide #
# by 2 and get the radius                               #
#########################################################
from sys import path, platform
from pathlib import Path

FREECAD_PATH = ''
DEFAULT_OUT_DIR = Path("~/Documents").expanduser()

# no extension!
# should be accesible tho
DEFAULT_FILE = "defaultNozzle"

if platform == 'win32':
    FREECAD_PATH = 'C:\\Program Files\\FreeCAD 1.1\\bin'
    print("[INFO] Platform: Windows")
    print("[INFO] If you get an incompatibility problem with a python.dll install that python version.")
    print("[INFO] ie. if it throws and error with python311.dll (or sth like that) you should install python 3.11")
elif platform == 'linux':
    FREECAD_PATH = '/usr/lib/freecad/lib'
elif platform == 'darwin':
    FREECAD_PATH = '/Applications/FreeCAD.app/Contents/Resources/lib'
    print("[INFO] Platform: Mac")
    print("[INFO] It *should* work, but it's not actively tested")
if FREECAD_PATH == '':
    print("OS not supported")
    print("(Supported platforms: Linux & Windows, MacOS should work tho)")
    print("If you know where the freecad library should be, you could edit this manually!")
    print("To do it just search for the module file and set the FREECAD_PATH variable to it instead of \'\'")
    exit()

path.append(FREECAD_PATH)

import FreeCAD as App
import Mesh

def openDefaultFile():
    print("[From Python] Opening default file...")
    try:
        App.openDocument(f"lib/pynef/cad_files/{DEFAULT_FILE}.FCStd")
        App.setActiveDocument(DEFAULT_FILE)
    except OSError:
        print("[From Python] Default file not found!")
        print(f"[From Python] Please check that the file {DEFAULT_FILE} exists!")
        print(f"[From Python] If it doesn't exist copy 'lib/pynef/cad_files/defaultNozzle.safe' to 'lib/pynef/cad_files/{DEFAULT_FILE}.FCStd'")
        return -1
    else:
        print("[From Python] Got file!")
        return 0

def updateNozzle(chamber_radius_mm:float, chamber_cone_length_mm:float, throat_radius_mm:float, exit_cone_length_mm:float, exit_radius_mm:float):
    App.ActiveDocument.Sketch.setDatum("ChamberRadius", App.Units.Quantity(f'{chamber_radius_mm} mm'))
    App.ActiveDocument.Sketch.setDatum("ChamberConeLength", App.Units.Quantity(f'{chamber_cone_length_mm} mm'))
    App.ActiveDocument.Sketch.setDatum("ThroatRadius", App.Units.Quantity(f'{throat_radius_mm} mm'))
    App.ActiveDocument.Sketch.setDatum("ExitConeLength", App.Units.Quantity(f'{exit_cone_length_mm} mm'))
    App.ActiveDocument.Sketch.setDatum("ExitRadius", App.Units.Quantity(f'{exit_radius_mm} mm'))
    print("[From Python] Updated sketch")

    App.ActiveDocument.recompute()
    print("[From Python] Recomputed file")
    App.ActiveDocument.save()
    print("[From Python] Saved file")
    return 0

def exportNozzle(file_name:str, file_type:str, target_dir = DEFAULT_OUT_DIR):
    print("[From Python] Exporting file...")
    file = file_name + "." + file_type
    nozzle = App.ActiveDocument.Body    
    Mesh.export([nozzle], f"{target_dir}/{file}")
    print(f"[From Python] Exported file to: {target_dir}/{file}")
    return 0
