# gcode-short-segments-cleaner
A small python script that can parse a gcode file and remove the short segments that are unecessary and can add visible marks on the surface.

# Introduction
The experience has shown that some 3D slicers for FDM process are generating poor quality gcode that contains a lot of short segments. These short segments are not needed for the part, they are actually slowing down the print head with the result of letting some visible marks on the outer surface. 

This issue has been observed in particular with Cura slicer in the scope of RC model plane which requires the specific cura surface slicing mode.

This script will parce the generated gcode and detect the short segments. It will comment the lines that are identified as unecessary and write the output into another gcode file.


# System requirement
This script has been written and tested with Python 3.11.8. But it is using only basic libraries and should work with any version of Python 3.


# How to use it
The current version is not providing any interactive interface. It is unecessary to execute the script from a command line interface.

The script takes two arguments:
- The path to the gcode file to convert
- The threshold of the minimum distance to detect the short segments, by default it is 0.08mm


Example:
$ python short_segments_cleaner.py -i my-generated-gcode-file.gcode

The script will write the output file to my-generated-gcode-file-fixed.gcode


# Contributing
Please feel free to give any feedback, comment, bug report or pull request.

