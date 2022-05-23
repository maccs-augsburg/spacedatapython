from PySide6.QtWidgets import (
    QMainWindow, QApplication, QLabel,
    QToolBar, QStatusBar, QCheckBox,
    QHBoxLayout, QVBoxLayout, QGridLayout,
    QLineEdit, QWidget, QFormLayout
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette, QColor

# class attributes are before init, they are like static variables?
# instance attributes are after init, they are unique to each one, more of what I want
class LineEdit(QLineEdit):
    ###########################################
    #Anything in here is a static variable#####
    ###########################################
    # this explains the super() keyword and various variations you might see used in tutorials
    #https://stackoverflow.com/questions/1607612/python-how-do-i-make-a-subclass-from-a-superclass
    def __init__(self):
        super().__init__()
        #########################################################################
        #Anything in here is an instance variable as long as it has self keyword#
        #########################################################################
        self.setMaxLength(7)
        self.textEdited.connect(self.text_edited)
        self.entry = "N/A"
    #######################################################################
    #Methods containing self, are instance methods#########################
    #######################################################################
    def text_edited(self, s):
        # s is a string, confirmed wity print(type(s))
        self.entry = s
        # Don't have to pass self again, implied, but weird
        print(self.get_entry())

    def get_entry(self):
        # TODO: Assert entries with QLineEdit methods, have to workaround Station Names 3 letters followed by numbers
        '''
        if XXX = letters then return as string

        if XXXXXX = all nums return as int
        '''
        return self.entry
    '''
    When we open a new file, want to reset the entries to some default value
    start min/sec/hour to (0, 0, 0)
    end min/sec/hour (23, 59, 59)
    '''
    def set_entry(self, new_entry):
        
        self.entry = new_entry

class Label(QLabel):
    def __init__(self, label_name):
        super().__init__()

        self.setText(label_name)
        font = self.font()
        font.setPointSize(12)
        self.setFont(font)
        self.setAlignment(Qt.AlignLeft)

class Color(QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)
    
# class EntryBox(LineEdit, Label):

#     def __init__(self, label_name):
#         super().__init__()

#         self.line_edit = LineEdit()
#         self.label = Label(label_name)

#         self.label.setBuddy(self.line_edit)