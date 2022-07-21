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

If unfamiliar with directorys and paths:

Run gui as usual inside spacedatapython folder.

```
python3 new_gui.py
```

All images are there and working since we are working off relative paths.

Now try running from one directory back.

```
cd ..
python3 spacedatapython/new_gui.py
```

The images don't appear anymore. We are using relative paths to our image files,
these paths are relative to the current working directory, not the folder the new_gui.py file is in.
So if you run script from somewhere else, it wont be able to find them.

-Make paths relative to the application instead of our current working directory

Inside new_gui.py at the top with imports 

```
# Packaging stuff
# Holds full path of the current Python File
# Use this to build relative paths for icons using os.path.join()
basedir = os.path.dirname(__file__)
```

New way to link to our images
Note: If you run this command again, images will now show up since we aren't linking images from our cwd.

``` 
python3 spacedatapython/new_gui.py
```

```
# Old way to link to images
action_savefile = QAction(QIcon("images/disk.png"),"Save File", self)
action_saveasfile = QAction(QIcon("images/disk.png"), "Save As...", self)

# New way to link to images
action_savefile = QAction(QIcon(os.path.join(basedir, "images", "disk.png")),"Save File", self)
action_saveasfile = QAction(QIcon(os.path.join(basedir, "images", "disk.png")), "Save As...", self)

```

Now that we have our application working from the root folder
We have to add our images to our dist/ directory. We can do this through command line
but since we have a lot of images, it would be better to modify the .spec file.

-open the MaccsApplication.spec folder. Under a = Analysis section:

Modify the "datas=" section as:

```
datas=[('images', 'images')],
```

Doing it this way, means that if we ever add more images we wont have to manually copy each file over.


# Building the App Bundle into a Disk Image #


