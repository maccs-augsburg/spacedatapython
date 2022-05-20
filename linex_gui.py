from ast import Pass
import sys
from PySide6.QtWidgets import (
    QMainWindow, QApplication, QLabel,
    QToolBar, QStatusBar, QCheckBox,
    QHBoxLayout, QVBoxLayout,
    QLineEdit, QWidget, QFormLayout
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon

class MainWindow(QMainWindow):

    def __init__(self):
        # Why does tutorial sometimes pass MainWindow, and other times it doesnt
        super(MainWindow, self).__init__()
        self.setWindowTitle("MACCS Stacked Plots")
        self.setWindowIcon(QIcon("maccslogo_870.jpeg"))
        
        main_layout = QHBoxLayout()
        entry_layout = QVBoxLayout()
        '''
        Add widgets to entry_layout
        '''
        station_line_edit = EntryBox("Station Code")
        # station_line_edit.setMaxLength(5)
        # station_line_edit.textEdited.connect(self.text_edited)
        # station_code = None
        # station_code_line_edit = EntryBox("Station Code: ")
        # entry_layout.addWidget(station_code_line_edit)
        entry_layout.addWidget(station_line_edit)
        main_layout.addLayout(entry_layout)

        widget = QWidget()
        widget.setLayout(main_layout)
        self.centralWidget(widget)
        
        # entry_layout.addWidget()
        # # QLine Edit, maybe I will use
        # def return_pressed(self):
        #     pass
        # def text_changed(self, s):
        #     # Assign s to station code, current entry in line_edit
        #     # Returns string value
        #     self.station_code = s

class LineEdit(QLineEdit):
    def __init__(self):
        super(LineEdit, self).__init__()

        self.setMaxLength(7)
        self.textEdited.connect(self.text_edited)
        self.entry

        def text_edited(self, s):
            pass

class EntryBox(QLineEdit, QLabel):

    entry = None
    # similar to constructor
    def __init__(self, label_name):
        super(EntryBox, self).__init__()

        self.setText(label_name)
        self.textEdited.connect(self.text_edited)
        # If it inherites from both, and we use QLabel.setBuddy to link to QLineEdit
        # Will this line even work? Purpose is to get qlable and qlineedit on the same line
        # vs. stacked
        self.setBuddy(self)

        def text_edited(self,s):
            entry = s


# class EntryBox(QLineEdit):

#     def __init__(self, label_name):
#         super(EntryBox, self).__init__()

#         label = QLabel(label_name)
#         # textEdited is a "signal", override corresponding method for custom us
#         #self.line_edit.textEdited.connect(self.text_edited)
#         self.textEdited.connect(self.text_edited)
#         self.setMaxLength(10)
#         entry = None

#         label.setBuddy(self)

#         def text_edited(self, s):
#             print("textEdited")
#             self.entry = s
        
#         def get_entry(self):
#             return self.entry


def main ():

    # use brackets if not using command line
    # app = QApplication(sys.argv)
    app = QApplication([])

    window = MainWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()