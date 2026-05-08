# What?
Basically a library to open a FreeCAD file with a default nozzle, update it's sketch and export it. All from python or C.

# Usage
## Python
Grab 'pynef' folder from lib/ and import it into you script. The example has documentation in spanish but it's pretty straight forward.
## C
Basically run make without arguments which will compile the library. If you want to run the C example use 'make example' and it will be in bin/

Then copy bin/pynef_cbinds.so and lib/pynef /to you lib/ folder in you project. Also, don't forget to grab the headers from c_binds/include.

Basically you should have something like:

| lib/
|---- pynef_cbinds.so
|---- pynef/ <-- python library
|
| src/
|---- include/
|-----|--- pynef_functions.h
|-----|--- pynef_types.
|---- main.c
