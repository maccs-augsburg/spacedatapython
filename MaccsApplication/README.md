## **Purpose**

To graph data retrieved from MACCS
magnetometer stations. Application
allows graphing of one overlayed graph with  
x, y, z axises or 3 stacked graphs. Currently
the application only supports raw .2hz data and
clean .s2 data.

## **Contents**

Application currently consists of 6 main files.

1. custom_widgets.py: Widgets with adjusted settings.
2. entry_checks.py: File to check user entries.
3. maccs_gui.py: Gui Application.
4. requirements.txt: File to install dependencies needed.
5. plot_three_axis_graphs.py: File to graph overlayed plots.
6. plot_stacked_graphs.py: File to graph axis on 3 different plots, stacked.

Note: Last two files are shared, so one directory back/up.

## **How to use**

## **Windows:**

**1st time using**

1. pip3 install PySide6
2. pip3 install matplotlib

**Run Program**

1. python3 maccs_gui.py

## **Mac:** 

Note: Had a lot of issues trying to install matplotlib and pyside6.

1. Install pipenv
2. Intall git
3. Create empty folder where you want application.
4. git clone https://github.com/maccs-augsburg/spacedatapython . (period intentional)
5. pipenv install -r path/to/requirements.txt
6. Run application from inside Maccs_Application folder

**Run Program**

1. python3 maccs_gui.py


**Note: To activate environment after closing out of window**

1. pipenv shell
2. Head to MaccsApplication folder
3. Run program

**Useful pipenv commands:**

If you add more dependecies, you should update the requirements file.

pipenv run pip freeze > requirements.txt

Installing/Uninstalling

pipenv install module
pipenv uninstall module



