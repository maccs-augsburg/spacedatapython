'''
custom_widgets.py

May 2022 -- Created -- Mark Ortega-Ponce
'''

from PySide6.QtWidgets import (
    QMainWindow, QLabel,
    QLineEdit, QWidget, QCheckBox, QPushButton,
    QSizePolicy, QSpinBox, QTimeEdit
)
from PySide6.QtCore import Qt, QTime
from PySide6.QtGui import QPalette, QColor

FONT_SIZE = 13
MINIMUM_HEIGHT = 25

class LineEdit(QLineEdit):
    '''
    '''

    def __init__(self):
        super().__init__()
        self.setMaxLength(5)
        # https://doc.qt.io/qt-5/qlineedit.html
        # Weird side effect,
        # Turns cursor black, and lets you put cursor in any spot inside the QLineEdit entries
        # It counts empty spaces as part of the limit, so could be annoying deleting blank spaces
        self.setInputMask("99999")
        self.textEdited.connect(self.text_edited)
        self.setAlignment(Qt.AlignCenter)
        #self.setAlignment(Qt.AlignLeft)
        self.entry = "N/A"
        self.setMaximumWidth(95)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMaximumHeight(MINIMUM_HEIGHT)

    def text_edited(self, s):
        self.entry = s
        #print(self.get_entry())

    # Wrapper around getter for QLineEdit, can also decide not to use and refactor with ide
    # Chose this because method name is more memorable
    def get_entry(self):
        return self.text()

    # Same situation here, want to keep the continuity in naming
    def set_entry(self, new_entry):

        self.entry = str(new_entry)
        self.setText(str(new_entry))


class Label(QLabel):
    def __init__(self, label_name):
        super().__init__()

        self.setText(label_name)
        font = self.font()
        font.setPointSize(FONT_SIZE)
        self.setFont(font)
        self.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.setMaximumWidth(85)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        #self.setMaximumHeight(MINIMUM_HEIGHT)

class CheckBox(QCheckBox):
    def __init__(self, label_name):
        super().__init__()

        self.setText(label_name)
        font = self.font()
        font.setPointSize(FONT_SIZE)
        self.setFont(font)
        self.setMaximumWidth(30)
        self.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        #self.setMinimumHeight(MINIMUM_HEIGHT)

class PushButton(QPushButton):
    def __init__(self, label_name, alternate_name):
        super().__init__()

        self.setText(label_name)
        font = self.font()
        self.setFont(font)
        font.setPointSize(FONT_SIZE)
        self.setCheckable(True)
        self.button_is_checked = False
        self.clicked.connect(self.button_toggle)
        self.setChecked(self.button_is_checked)
        self.setMaximumWidth(145)#145
        self.alternate_name = alternate_name
        self.original_name = label_name
        #self.setMaximumHeight(30)
        #self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        #self.setMinimumHeight(MINIMUM_HEIGHT)
        #self.setMaximumWidth(95)

    def button_toggle(self, checked):
        self.button_is_checked = checked
        #print(self.button_is_checked)
        self.change_text()
    
    def is_toggled(self):
        return self.button_is_checked

    def change_text(self):

        checked = self.is_toggled()

        if not checked:
            self.setText(self.original_name)
        else:
            self.setText(self.alternate_name)

    def set_toggle_status_false(self):
        self.button_is_checked = False
        self.setChecked(False)

class Spinbox(QSpinBox):
    #https://doc.qt.io/qt-5/qspinbox.html#textChanged
    def __init__(self, min_value, max_value, step_size):
        super().__init__()

        font = self.font()
        self.setFont(font)
        font.setPointSize(FONT_SIZE)
        #self.setMinimum(min_value)
        #self.setMaximum(max_value)
        self.setRange(min_value, max_value)
        self.setSingleStep(step_size)
        self.setWrapping(True)

        self.valueChanged.connect(self.value_changed)
        self.setAlignment(Qt.AlignCenter)
        #self.setAlignment(Qt.AlignLeft)
        self.entry = 0
        self.setMaximumWidth(95)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMaximumHeight(MINIMUM_HEIGHT)

    def value_changed(self, i):
        self.entry = i
        #print("Seeing if signal works", self.entry, "type: ",type(self.entry))
        #print(str(self.get_entry()))
        #print(type(self.get_entry()))

    # Wrapper around getter for QLineEdit, can also decide not to use and refactor with ide
    # Chose this because method name is more memorable
    def get_entry(self):
        # returns int
        #return self.text() # this works for some reason, copied over from line edit class, shouldnt work?
        # this is in the documentation self.value(), but gives errors
        return self.entry

    # Same situation here, want to keep the continuity in naming
    def set_entry(self, new_entry):
        #print(new_entry, " : type : ", type(new_entry))
        # emits valueChanged signal if new entry is different from old one
        self.setValue(new_entry)

class Time(QTimeEdit):
    # http://man.hubwiz.com/docset/Qt_5.docset/Contents/Resources/Documents/doc.qt.io/qt-5/qtimeedit.html
    # http://man.hubwiz.com/docset/Qt_5.docset/Contents/Resources/Documents/doc.qt.io/qt-5/qdatetimeedit.html#timeChanged
    # http://man.hubwiz.com/docset/Qt_5.docset/Contents/Resources/Documents/doc.qt.io/qt-5/qdatetimeedit.html#time-prop
    def __init__(self):
        super().__init__()
        self.min_time = QTime(0,0,0)
        self.max_time = QTime(23,59,59)
        self.time = QTime(0,0,0)
        self.hour = 0
        self.minute = 0
        self.second = 0
        font = self.font()
        self.setFont(font)
        font.setPointSize(FONT_SIZE)
        self.setAlignment(Qt.AlignCenter)
        self.setMaximumWidth(95)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMaximumHeight(MINIMUM_HEIGHT)
        self.setTimeRange(self.min_time, self.max_time)
        self.setDisplayFormat("hh:mm:ss")
        self.timeChanged.connect(self.time_changed)
    
    def time_changed(self, time):
        self.time = time
        # inherited function from QDateTimeEdit
        self.hour = self.time.hour()
        self.minute = self.time.minute()
        self.second = self.time.second()
        
    def get_hour(self):
        return self.hour
    def get_minute(self):
        return self.minute
    def get_second(self):
        return self.second

    def set_start_time(self):
        self.setTime(self.min_time)
    def set_end_time(self):
        self.setTime(self.max_time)
        
class Color(QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)