# README - MACCS Space Data Python #

This directory contains python3 scripts which process MACCS data.

### What is this repository for? ###

* The scripts here can be used to process MACCS data; examining,
converting, and graphing the data files.
* Version 0.3 - 29 June 2020

### How do I get set up? ###

* Each python file with a name beginning in cl_ should contain the code
to operate as a Unix-style command line utility. Many files contain only 
utility functions. Some may contain tests.
* new_gui.py is a GUI program.
* All files must be written in python3.
* Libraries used now include matplotlib and Pillow. Run pip3 install
(matplotlib | Pillow) if not included already.

### What is here? ###

* documentation/  This folder contains notes and other documentation
**  BinaryFormatNotes.txt: Notes about the binary format of .2hz files.
* gui/ This folder contains gui code, dependent on PySide6
* images/ This folder contains images used in the gui
* model/ This folder contains code to read and interpret MACCS data files
** raw_codecs.py: This contains code to convert various parts of the
raw files into and out of integer and float values.
* plot/ Contains the plotting code, dependent on matplotlib
* testdata/ Contains MACCS data files for testing
* util/ Contains modules with functions for file naming
** station_names.py: Functions converting between two, three, and four letter
station abbreviations along with short and long names.
* clean_to_screen.py: A program to print the contents of a cleaned 2hz file to
the screen.
* raw_to_iaga2002.py: A program to write the contents of a 2hz file to a text
file in the IAGA 2002 format.
* raw_to_screen.py: A program to print the contents of a 2hz file to
the screen.
* README.md: This file.
* TODO.md: Suggestions for programs and functions to write for this project.

### Who do I talk to? ###

* Erik Steinmetz: maccs@augsburg.edu, steinmee@augsburg.edu
