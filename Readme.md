# GUI
This is first just in case: a GUI is in development, it will be kept in the 'main-gui' branch. If you want to use it just change the branch to it in the upper left corner of the file view and download the code like normal. Then run pynef_gui.py.

# What?
Basically a library to open a FreeCAD file with a default nozzle, update it's sketch and export it. All from Python or C. It doesn't do math, it just takes the nozzle parameters and spits out a 3D file. In case you don't know/care how to do the math py_input_example shows the 3 variables you need to input that are easily obtainable. Basically just copy that code and change you the input goes in. Chamber diameter, at least for us, is a design constraint, Ac/At is something to maybe experiment with (following Rocket Propulsion Elements 9th ed. a value higher than 3 should be ok). Ae/At is obtainable via various methods, we are using CEA. (Actually [CAT-ME](https://github.com/Bloody-Ari/CAT-ME), but it's kind of a CEA wrapper).

# How?
Pynef uses a fundamental design choice of FreeCAD to it's advantage, FreeCAD works in a way that you can fully control it from Python. In this case, pynef opens a .FCStd file, selects a sketch, modifies it's constraints, and exports it. You have three functions:

| Function        | Arguments                                                                                                | Description                                                                                                                                             |
|-----------------|----------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------|
| openDefaultFile |                                                                                                          | Opens and sets lib/pynef/cad_files/defaultNozzle.FCStd as the active file.                                                                              |
| updateNozzle    | chamber radius, chamber cone length, throat radius,  exit cone length, exit radius all inputs are in mm) | Selects sketch "Sketch" from the file and changes named datums corresponding to the arguments. This function recomputes ("reloads") and saves the file. |
| exportNozzle    | file name, file type, target directory (optional, without /)                                             | Exports with file name and type, we use 3mf and stl.                                                                                                    |

All functions return 0 on success.

# Usage

## Python

Grab 'pynef' folder from lib/ and import it into you script. The example has documentation in spanish but it's pretty straight forward. (The code is one Python file tho).

py_example.py simply calls the 3 library functions to modify the CAD file.

py_input_example.py uses a few formulas to go from Ac/At, Ae/At, and chamber diameter to the required information. It basically does the math.

## C
Basically run make without arguments which will compile the library. If you want to run the C example use 'make example' and it will be in bin/

Then copy bin/pynef_cbinds.so and lib/pynef to you lib/ folder in you project. Also, don't forget to grab the headers from c_binds/include.

You should have something like this:

| lib/

|---- pynef_cbinds.so

|---- pynef/ <-- python library

|

| src/

|---- include/

|-----|--- pynef_functions.h

|-----|--- pynef_types.h

|---- main.c
