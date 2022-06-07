
class RadioButtons(QtWidgets.QWidget):
    """
    Custom widget for my radio buttons for three axis graph display
    """
    def __init__(self):
        super().__init__()
        #######################
        ### Checkbox Select ###
        #######################

        self.checkbox_plotx = QCheckBox("X Plot", self)
        self.checkbox_ploty = QCheckBox("Y Plot", self)
        self.checkbox_plotz = QCheckBox("Z Plot", self)

        
class CustomToolbar(NavigationToolbar2QT):
    def __init__(self, canvas):
        NavigationToolbar2QT.__init__(self,canvas)
        FINAL_REMOVE_SUBPLOT_INT = 6
        self.DeteleToolByPos(FINAL_REMOVE_SUBPLOT_INT)
