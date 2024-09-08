from PySide6.QtWidgets import *
import sys, json, os

file_output = 'test.json'

class Tokens():
    def __init__(self):
        self.tokens = {
			'age': {'type': 'spinbox', 'label': 'Age', 'datatype': 'int', 'default': 0, 'group':  'Amazing'},
			'sports': {'type': 'combobox', 'label': 'Degree', 'options' : ['Volleyball', 'Rock climbing', 'SCUBA'], 'datatype': 'str', 'default': 'Basket weaving', 'group': 'Cool'},
			'name': {'type': 'lineedit', 'label': 'Name', 'datatype': 'str', 'default': '', 'group': 'Lame'},
            'tree': {'type': 'combobox', 'label': 'Tree', 'options' : ['Pine', 'Maple', 'Palm'], 'datatype': 'str', 'default': 'Basket weaving', 'group': 'Cool'},
            'sleeping': {'type': 'checkbox', 'label': 'Sleeping', 'datatype': 'bool', 'default': False, 'group': 'Lame'}
			}
        self.config = {}

class Window(QDialog):
	# constructor
    def __init__(self):
        super(Window, self).__init__()
        self.setWindowTitle("PySide Token Test 1")
        token_groups = ['Lame', 'Cool', 'Amazing']
        self.setGeometry(100, 100, 300, 400)
        self.layout = QFormLayout()

        self.tok = Tokens()
        
        self.formGroupBoxes = {}
        
        for this_token_group in token_groups:
            self.draw_group_box(this_token_group)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonBox.accepted.connect(self.write_info_to_file)
        self.buttonBox.rejected.connect(self.reject)
        
        mainLayout = QVBoxLayout()
        for item in self.formGroupBoxes:
            mainLayout.addWidget(self.formGroupBoxes[item][0])
        mainLayout.addWidget(self.buttonBox)
        self.setLayout(mainLayout)

        self.read_info_from_file(file_output)

        x = 2

    def read_info_from_file(self, filename):
        file_exists = os.path.exists(filename)
        if file_exists:
            with open(filename, 'r') as f:
                self.config = json.load(f)
            for key, val in self.config.items():
                gui_component = getattr(self, key)
                if self.tok.tokens[key]['type'] in ['spinbox']:
                    gui_component.setValue(int(val))
                elif self.tok.tokens[key]['type'] in ['combobox']:
                    gui_component.setCurrentText(val)
                elif self.tok.tokens[key]['type'] in ['lineedit']:
                    gui_component.setText(val)
                elif self.tok.tokens[key]['type'] in ['checkbox']:
                    gui_component.setChecked(bool(val))
		
    def draw_group_box(self, group_name):
        this_group_box = QGroupBox(group_name)
        self.formGroupBoxes[group_name] = [this_group_box,  QFormLayout()]
        for key, value in self.tok.tokens.items():
            if value['group'] == group_name:
                if value['type'] == 'spinbox':
                    setattr(self, key, QSpinBox())
                    obj = getattr(self, key)
                elif value['type'] == 'combobox':
                    setattr(self, key, QComboBox())
                    obj = getattr(self, key)
                    obj.addItems(value['options'])
                elif value['type'] == 'lineedit':
                    setattr(self, key, QLineEdit())
                    obj = getattr(self, key)
                elif value['type'] == 'checkbox':
                    setattr(self, key, QCheckBox())
                    obj = getattr(self, key)
                self.formGroupBoxes[group_name][1].addRow(QLabel(value['label']), obj)  #add row to layout
        self.formGroupBoxes[group_name][0].setLayout(self.formGroupBoxes[group_name][1])

	# run writeInfo method when form is accepted
    def write_info_to_file(self):
        data_dict = {}
        for key, val in self.tok.tokens.items():
            if val['type'] in ['lineedit']:
                result = getattr(self, key).text()
            elif val['type'] in ['spinbox']:
                result = getattr(self, key).text()
            elif val['type'] in ['combobox']:
                result = getattr(self, key).currentText()
            elif val['type'] in ['checkbox']:
                result = getattr(self, key).isChecked()
            else:
                result = 'ERROR, UNKNOWN TYPE!!'
            print(val['label'] +': ' + str(result))
            data_dict[key] = result
        with open(file_output, 'w') as f:
            json.dump(data_dict, f)
        self.close()


# main method
if __name__ == '__main__':
	app = QApplication(sys.argv)
	window = Window()
	window.show()
	sys.exit(app.exec())
