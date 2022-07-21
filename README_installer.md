# Guide for packaging python applications #


[Tutorial Windows](https://www.pythonguis.com/tutorials/packaging-pyside6-applications-windows-pyinstaller-installforge/)
[Tutorial Macbook](https://www.pythonguis.com/tutorials/packaging-pyqt5-applications-pyinstaller-macos-dmg/)

Important: You always need to compile your app on your target system. So, if you want to create a Mac .app
    you need to do this on a Mac, for an EXE you need to use windows.
    
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
    1. Dist also contains the .exe file you can use to run your application, should be named MaccsApplication.
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

Note:
MacOS app bundles you need to provide an .icns file for the icon
This link is to an app that can convert an image to .icns form [App Store](https://apps.apple.com/us/app/image2icon-make-your-own-icons/id992115977)
This link is to a windows tool to create .ico file [Windows Tool](https://portableapps.com/apps/graphics_pictures/icofx_portable)

```
pyinstaller --windowed --icon="images/maccs_logo.ico/icns" new_gui.py
```

Can alternatively modify the MaccsApplication.spec file inside spacedatapython folder
Under App Section: Modify the icon="images/your_image.icns/ico" - images/ is put in front to be
able to find the image since the MaccsApplication.spec file is one directory up.
Run following command to build app again, and see changes

```
pyinstaller MaccsApplication.spec
```

# Adding our images as data files and resources #

Currently as it sits, our app does not have the maccs logo, or the toolbar icons visible.
