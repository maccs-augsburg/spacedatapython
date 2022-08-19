# Setting up windows to make windows installer #

Need following installed

Install git [git for windows](https://git-scm.com/download/win)

Install python [python for windows](https://www.python.org/downloads/windows/) (using 3.10.6 at time of writing)

Install forge [install forge](https://installforge.net/download/) (using 1.4.2 at time of writing)

Note: Have to manually add python to environment variables, or wont be able to use in command prompt

Find python installer in downloads folder.

- Open the file, it should prompt you with ("Modify Setup")
- Click on 'Modify' option
- You'll be prompted with 'Optional features window'
- Hit next
- Check the 'Add Python to environment variables' checkbox
- Then hit install

Check python version is working in command prompt: ```python -V```

## Setting up environment ##

1. Clone the git repo onto the Desktop with following command, left out dot intentionally.

```
git clone https://github.com/maccs-augsburg/spacedatapython
```

2. Cd back to home directory (not sure if it matters where you install) and install pipenv.
Note: Python installer will include a pip install automatically.

```
pip install pipenv
```

Check pipenv is working by typing ```pipenv```. You should get a help section.

3. Cd back into spacedatapython folder located on the Desktop directory.
Set up pipenv environment with requirements.txt file found in documentation folder.

```
cd Desktop
```

```
cd spacedatapython
```

```
pipenv install -r documentation/requirements.txt
```

4. Activate environment

```
pipenv shell
```

Note: You will see (spacedatapython-some_weird_hex_values) before your directory
in command prompt. This indicates your in the python environment.

## Setting up installer ##

1. Install pyinstaller.

```
pipenv install pyinstaller
```

2. Check pyinstaller is working by typing ```pyinstaller```. You'll get a help section if it does.

3. Make build and dist folder with pyinstaller inside spacedatapython and provide the windows.spec file.

```
pyinstaller MaccsPlotter_windows.spec
```

4. You should see a build and dist folder now.
Inside the dist folder, there will be a folder called 'MACCS Plotter'.
All dependencies are inside here.


## Setting up install forge ##

1. Open install forge

2. Below the taskbar there should be an option to open a file.

3. Open the 'windows_installer_settings.ifp' file. This contains all the settings for making the installer.
This way I don't have to manually add all the files and folders inside dist/MACCS Plotter in the file section of install forge.

4. If your path to spacedatapython folder is the same as mine, (C:\Users\Administrator\Desktop\spacedatapython>),
then making the installer will go smoothly. If not, take a look at how_to_update_windows_installer.md file inside documentation folder.

5. Click on build, install forge will put the new wizard inside the installers folder,
provided your path is the same as mine. If it's not you will have to modify the paths, inside the build section.

6. I got an error 'Could not archive folder: setuptools-64.0.3.dist-info'

7. I left out the part where I added all files and folders in install forge located inside dist/MACCS Plotter folder,
I mention some of this in the how_to_update_windows_installer.md documentation.

8. Fixing the error. I head to Setup section in InstallForge, click on files tab.

9. Find the folder that is stoping InstallForge from completing the build.

10. Click on the folder, and select 'remove' from the toolbar.

11. Add the folder back in, click 'add folder' from the toolbar.

12. You'll get a finder like window. Head to spacedatapython/dist/MACCS Plotter/

13. Find the folder that was giving us issues.

14. New folder is 'setuptools-65.1.0.dist-info' (at time of writing)

15. Error explained: Could not find folder, so it stopped whole build. This might happen often since setup-tools is updated frequently.

16. Hit build again.

17. Build was successful.

18. New installer should be inside the installers folder.
