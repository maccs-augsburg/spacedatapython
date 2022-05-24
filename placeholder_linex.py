        self.plot_min_x = QLabel("Plot Min x: ")
        self.plot_max_x = QLabel("Plot Max x: ")

        self.plot_min_y = QLabel("Plot Min y: ")
        self.plot_max_y = QLabel("Plot Max y: ")

        self.plot_min_z = QLabel("Plot Min z: ")
        self.plot_max_z = QLabel("Plot Max z: ")

        self.input_min_x = QLineEdit()
        self.input_max_x = QLineEdit()

        self.input_min_y = QLineEdit()
        self.input_max_y = QLineEdit()

        self.input_min_z = QLineEdit()
        self.input_max_z = QLineEdit()

        self.input_min_x.setMaximumWidth(50)
        self.input_max_x.setMaximumWidth(50)
        self.input_min_y.setMaximumWidth(50)
        self.input_max_y.setMaximumWidth(50)
        self.input_min_z.setMaximumWidth(50)
        self.input_max_z.setMaximumWidth(50)

        self.label_and_entry_layout.addWidget(self.plot_min_x, 8,0)
        self.label_and_entry_layout.addWidget(self.plot_max_x, 9,0)
        
        self.label_and_entry_layout.addWidget(self.plot_min_y, 10,0)
        self.label_and_entry_layout.addWidget(self.plot_max_y, 11,0)

        self.label_and_entry_layout.addWidget(self.plot_min_z, 12,0)
        self.label_and_entry_layout.addWidget(self.plot_max_z, 13,0)

        self.label_and_entry_layout.addWidget(self.input_min_x, 8,1)
        self.label_and_entry_layout.addWidget(self.input_max_x, 9,1)
        
        self.label_and_entry_layout.addWidget(self.input_min_y, 10,1)
        self.label_and_entry_layout.addWidget(self.input_max_y, 11,1)

        self.label_and_entry_layout.addWidget(self.input_min_z, 12,1)
        self.label_and_entry_layout.addWidget(self.input_max_z, 13,1)