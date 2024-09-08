from PySide6.QtWidgets import *
import sys, json, os

from PySide6.QtCore import QAbstractTableModel, Qt
import pandas as pd

file_output = 'test.json'

class Tokens():
    def __init__(self):
        self.tokens = {
			'age': {'type': 'spinbox', 'label': 'Age', 'datatype': 'int', 'default': 0, 'group':  'Amazing'},
			'sports': {'type': 'combobox', 'label': 'Degree', 'options' : ['Volleyball', 'Rock climbing', 'SCUBA'], 'datatype': 'str', 'default': 'Basket weaving', 'group': 'Cool'},
			'name': {'type': 'lineedit', 'label': 'Name', 'datatype': 'str', 'default': '', 'group': 'Lame'},
            'tree': {'type': 'combobox', 'label': 'Tree', 'options' : ['Pine', 'Maple', 'Palm'], 'datatype': 'str', 'default': 'Basket weaving', 'group': 'Cool'},
            'sleeping': {'type': 'checkbox', 'label': 'Sleeping', 'datatype': 'bool', 'default': False, 'group': 'Lame'},
            'story': {'type': 'plaintextedit', 'label': 'Story', 'datatype': 'str', 'default': 'It was a dark and stormy night.', 'group':  'Amazing'},
            'table1': {'type': 'table', 'label': 'Roses', 'datatype': 'tabular', 'data': [['Pink', 20, 'B+'], ['Red', 15, 'A-']], 'columns': ['Color', 'Thorn count', 'Fanciness'], 'optional_row_labels': [], 'row_count': 10, 'group': 'Lame'},
            'table2': {'type': 'table', 'label': 'AIs', 'datatype': 'tabular', 'data': [['Samsung', 5], ['Apple', 2]], 'columns': ['Maker', 'IQ'], 'optional_row_labels': ['Bixby', 'Siri'], 'row_count': 2, 'group': 'Cool'}
			}
        self.config = {}

class TableModel(QAbstractTableModel):
    def __init__(self, data_table, row_count, column_headings, row_headings = []):
        super(TableModel, self).__init__()
        self.data_table = data_table
        num_cols = len(column_headings)
        while len(self.data_table) < row_count:
            self.data_table.append(['' for ix in range(num_cols)])
        self._row_count = row_count
        self._column_headings = column_headings
        self._row_headings = row_headings
    def data(self, index, role):
        if role == Qt.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            return self.data_table[index.row()][index.column()]
    def rowCount(self, index):
        # The length of the outer list.
        return self._row_count
    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self.data_table[0])
    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._column_headings[section])
            if orientation == Qt.Vertical:
                if self._row_headings and len(self._row_headings) == self._row_count:
                    return str(self._row_headings[section])
                else:
                    return str(section)
    def flags(self, index):
        return Qt.ItemIsSelectable|Qt.ItemIsEnabled|Qt.ItemIsEditable
    def setData(self, index, value, role):
        if role == Qt.EditRole:
            self.data_table[index.row()][index.column()] = value
            return True

class Window(QDialog):
	# constructor
    def __init__(self):
        super(Window, self).__init__()
        self.setWindowTitle("PySide Token Test 1")
        token_groups = ['Lame', 'Cool', 'Amazing']
        self.setGeometry(100, 100, 700, 500)
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
        self.set_config()

        print(self.tok.config)

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
                elif value['type'] == 'plaintextedit':
                    setattr(self, key, QPlainTextEdit())
                    obj = getattr(self, key)
                elif value['type'] == 'table':
                    setattr(self, key, QTableView())
                    obj = getattr(self, key)
                    obj.setModel(TableModel(data_table = value['data'], row_count = value['row_count'], column_headings = value['columns'], row_headings = value['optional_row_labels']))
                              
                self.formGroupBoxes[group_name][1].addRow(QLabel(value['label']), obj)  #add row to layout
        self.formGroupBoxes[group_name][0].setLayout(self.formGroupBoxes[group_name][1])

    def set_config(self):
	# run writeInfo method when form is accepted
        for key, val in self.tok.tokens.items():
            if val['type'] in ['lineedit']:
                result = getattr(self, key).text()
            elif val['type'] in ['spinbox']:
                result = getattr(self, key).text()
            elif val['type'] in ['combobox']:
                result = getattr(self, key).currentText()
            elif val['type'] in ['checkbox']:
                result = getattr(self, key).isChecked()
            elif val['type'] in ['plaintextedit']:
                result = getattr(self, key).toPlainText()
            elif val['type'] in ['table']:
                result = getattr(self, key).model().data_table
            else:
                result = 'ERROR, UNKNOWN TYPE!!'
            self.tok.config[key] = result
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
                elif self.tok.tokens[key]['type'] in ['plaintextedit']:
                    gui_component.setPlainText(val)
                elif self.tok.tokens[key]['type'] in ['table']:
                    gui_component.model().data_table = val

	# run writeInfo method when form is accepted
    def write_info_to_file(self):
        self.set_config()
        with open(file_output, 'w') as f:
            json.dump(self.tok.config, f)
        self.close()


# main method
if __name__ == '__main__':
	app = QApplication(sys.argv)
	window = Window()
	window.show()
	sys.exit(app.exec())
