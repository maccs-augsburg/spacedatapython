from ast import Pass
import sys
from PySide6.QtWidgets import (
    QMainWindow, QApplication, QLabel,
    QToolBar, QStatusBar, QCheckBox,
    QHBoxLayout, QVBoxLayout,
    QLineEdit, QWidget, QFormLayout
)
from PySide6.QtCore import Qt

class MainWindow(QMainWindow):

    def __init__(self):
        # Why does tutorial sometimes pass MainWindow, and other times it doesnt
        super(MainWindow, self).__init__()
        self.setWindowTitle("MACCS Stacked Plots")
        
        main_layout = QHBoxLayout()
        entry_layout = QVBoxLayout()
        entry_form_layout = QFormLayout()
        '''
        Add widgets to entry_layout
        '''
        # self.station_line_edit = QLineEdit()
        # self.station_line_edit.setMaxLength(5)
        # self.station_line_edit.textEdited.connect(self.text_edited)
        # self.station_code = None
        station_code_line_edit = LineEdit()
        entry_form_layout.addRow("Station Code: ")
        
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
        self.station_line_edit.textEdited.connect(self.text_edited)
        self.entry = None

        def text_edited(self, s):
            print("textEdited")
            self.entry = s
        
        def get_entry(self):
            return self.entry


def main ():

    # use brackets if not using command line
    # app = QApplication(sys.argv)
    app = QApplication([])

    window = MainWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()