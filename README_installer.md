# Guide for packaging python applications #


[Tutorial](https://www.pythonguis.com/tutorials/packaging-pyside6-applications-windows-pyinstaller-installforge/)

## Install PyInstaller (Popular tool for packaging python applications) ##

```
pip3 install PyInstaller
```

Note: If there are problems with packaing the application, update PyInstaller

```
pip3 install --upgrade PyInstaller pyinstaller-hooks-contrib
```

Run this next command inside spacedatapython folder, new_gui.py should be inside this folder.

```
pyinstaller --noconsole --name "MaccsApplication" new_gui.py
```

You will generate 2 directories and one file with this command: 
1. dist - contains everything to run your application, application and libraries that is uses
2. build - can be ignored for the most part, contains results of analysis? Some logs of the building, might be useful for debugging
3. MaccsApplication.spec - You can modify the .spec file instead of passing arguments to pyinstaller

Note:

If you modify anything, to see the changes, you will have to run.

```
pyinstaller MaccsApplication.spec
```

This rebuilds your application with the new settings.

noconsole flag is passed so console window doesn't open when running the .exe file located inside dist folder
the exe file will have the name passed through, so MaccsApplication.exe

# Changing the icon from python to Maccs Logo #

