# Guide for packaging python applications #


[Tutorial Windows](https://www.pythonguis.com/tutorials/packaging-pyside6-applications-windows-pyinstaller-installforge/)

[Tutorial Macbook](https://www.pythonguis.com/tutorials/packaging-pyqt5-applications-pyinstaller-macos-dmg/)

[Tutorial Linux](https://www.pythonguis.com/tutorials/packaging-pyqt5-applications-linux-pyinstaller/)


Important: You always need to compile your app on your target system. So, if you want to create a Mac .app
    you need to do this on a Mac, for an EXE you need to use windows.


## Install PyInstaller ##

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

--noconsole flag (indicates to not open console window on startup of app)
--name flag (indicates the name for the .exe, .app)

## Change from Python Icon to MACCS logo and make images work with .app and .exe ##

After running the pyinstaller command in previous step, there should be a file
called MaccsApplication.spec file, or whatever name you passed through.

Note: 

Windows uses .ico logo, Mac uses .icns format. Relevant links to convert Maccs Logo: \

Put in images folder once converted.

[App Store](https://apps.apple.com/us/app/image2icon-make-your-own-icons/id992115977)
[Windows Tool](https://portableapps.com/apps/graphics_pictures/icofx_portable)

Open the .spec file and under App Section: Modify the icon="images/your_image.icns/ico" (Changes logo from python to Maccs)

Under the nalysis section modify "datas=" as:

```
datas=[('images', 'images')],
```

After making changes to .spec file, you should build the app again.
Can do this by running next command.

```
pyinstaller MaccsApplication.spec
```

# Creating Installer for Windows #

TODO: Can't follow windows tutorial up to here, need to install forge.
