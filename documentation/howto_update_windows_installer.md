# Updating Windows Executable Setup Wizard #

## Windows ##

For updating the executable file inside the installers folder when main code is updated:

1. You should have a MaccsPlotter_windows.spec file already. If it's gone, try following installer README or look at old branches.

2. You will need to install InstallForge if this is your first time updating the executable.

Download [InstallForge](https://installforge.net/)

3. There should be a file called ```windows_installer_settings.ifp``` This file is used to restore the settings for the application.

Note: Unless your project is in the same path as here: ```C:\Users\Administrator\Desktop\spacedatapython\dist\MACCS Plotter\``` you will have to re-add all the files and folders located inside dist folder into InstallForge. If you don't you will get errors that it can't archive some dependencies. If you are having this issue, scroll to the bottom of the tutorial and follow along the installforge section. OR open up the .ifp file in some text editor, and search and replace ```C:\Users\Administrator\Desktop\spacedatapython\dist\MACCS Plotter\``` with your path, up to the dist/MACCS Plotter\ part specifically. You will need to build the application to see these files on your computer (not being pushed up to github). ```pyinstaller MaccsPlotter_windows.spec```

[Tutorial Windows](https://www.pythonguis.com/tutorials/packaging-pyside6-applications-windows-pyinstaller-installforge/)


If all these requirements are met:

1. Update the windows build and dist folders. If you have any previous versions from a different os, I would just delete them first.

```
pyinstaller MaccsPlotter_windows.spec
```

2. Open install forge and open the .ifp file called ```windows_installer_setting.ifp```
    Once open, click on build by the toolbar icons. Once it's done you should have the new executable in the installers folder (this path can be changed from the build section)
