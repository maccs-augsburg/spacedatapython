# Guide for packaging python applications #


[Tutorial Windows](https://www.pythonguis.com/tutorials/packaging-pyside6-applications-windows-pyinstaller-installforge/)

[Tutorial Macbook](https://www.pythonguis.com/tutorials/packaging-pyqt5-applications-pyinstaller-macos-dmg/)

[Tutorial Linux](https://www.pythonguis.com/tutorials/packaging-pyqt5-applications-linux-pyinstaller/)

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

-open the MaccsApplication.spec file. Under a = Analysis section:

Modify the "datas=" section as:

```
datas=[('images', 'images')],
```

Doing it this way, means that if we ever add more images we wont have to manually copy each file over.

# Creating an Installer for Windows #

Download [InstallForge](https://installforge.net/)

TODO: Can't follow windows tutorial up to here, need to install forge

Seems more straightforward than mac though


# Creating a Linux Package (Ubuntu Deb) #

(On Ubuntu and Debian, packages are named .deb files, redhat names them .rpm, arch linux names them .pacman)

Can build one and it will work for all of these.

### Install fpm ###

```
# Install this first
sudo apt-get install ruby
# After installing ruby
gem install fpm --user-install

# If you see a warning e.g. 
You don't have /home/martin/.local/share/gem/ruby/2.7.0/bin in your PATH 
you will need to add that to your path in your .bashrc file.

# Check fpm is working
fpm --version
```

# Building the App Bundle into a Disk Image for Apple#

We could share the app as is for apple, but that would mean unpacking 100's of files,
this is not usual behavior for downloading anything for macOs.

For macOs install create-dmg with homebrew:

```
brew install create-dmg
```

If you dont have homebrew, check out the github page for instructions [Github create-dmg](https://github.com/create-dmg/create-dmg)


Make sure build is ready before creating a disk image

```
pyinstaller MaccsApplication.spec
```

Create recommended shell script found in tutorial: (Modifying for differences in names and target system - Windows/Mac/Linux)

```
#!/bin/sh
# Create a folder (named dmg) to prepare our DMG in (if it doesn't already exist).
mkdir -p dist/dmg
# Empty the dmg folder.
rm -r dist/dmg/*
# Copy the app bundle to the dmg folder.
cp -r "dist/Hello World.app" dist/dmg
# If the DMG already exists, delete it.
test -f "dist/Hello World.dmg" && rm "dist/Hello World.dmg"
create-dmg \
  --volname "Hello World" \
  --volicon "Hello World.icns" \
  --window-pos 200 120 \
  --window-size 600 300 \
  --icon-size 100 \
  --icon "Hello World.app" 175 120 \
  --hide-extension "Hello World.app" \
  --app-drop-link 425 120 \
  "dist/Hello World.dmg" \
  "dist/dmg/"
```

Example modifications I made to make it work with our project.

```
#!/bin/sh
# Create a folder (named dmg) to prepare our DMG in (if it doesn't already exist).
mkdir -p dist/dmg
# Empty the dmg folder.
rm -r dist/dmg/*
# Copy the app bundle to the dmg folder.
cp -r "dist/MaccsApplication.app" dist/dmg
# If the DMG already exists, delete it.
test -f "dist/MaccsApplication.dmg" && rm "dist/MaccsApplication.dmg"
# Window settings, dictate size of dmg installer window
create-dmg \
  --volname "MaccsApplication" \
  --volicon "images/maccslogo_nobg.icns" \
  --window-pos 200 120 \
  --window-size 600 300 \
  --icon-size 100 \
  --icon "MaccsApplication.app" 175 120 \
  --hide-extension "MaccsApplication.app" \
  --app-drop-link 425 120 \
  "dist/MaccsApplication.dmg" \
  "dist/dmg/"
```

Save this shell script at same level as new_gui.py folder.

Modify permissions for the shell script: (set the execute bit)

```
chmod +x builddmg.sh
```

Run this command to make image:

```
./builddmg.sh
```

For updating disk image when main code is updated:

```
pyinstaller MaccsApplication.spec
./builddmg_mac.sh
```
