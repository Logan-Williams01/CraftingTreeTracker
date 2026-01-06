import sys
from Item import Item
from Recipe import Recipe
from CraftingDatabase import CraftingDatabase
from PySide6.QtWidgets import QSpinBox, QLineEdit, QDialog, QMessageBox, QInputDialog, QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QLabel, QTabWidget, QListWidget, QHBoxLayout
from PySide6.QtCore import Qt

class ItemDialog(QDialog):
    def __init__(self, parent=None, title="Add Item", default_name="", default_id="", default_value=0, editing=False):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.editing = editing

        layout = QVBoxLayout()

        #Name field
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Name:"))
        self.name_input = QLineEdit(default_name)
        self.name_input.textChanged.connect(self.update_id_field)
        name_layout.addWidget(self.name_input)
        layout.addLayout(name_layout)

        #ID field
        id_layout = QHBoxLayout()
        id_layout.addWidget(QLabel("Item ID:"))
        self.id_input = QLineEdit(default_id)
        self.id_input.setDisabled(True)
        id_layout.addWidget(self.id_input)
        layout.addLayout(id_layout)

        if editing:
            note = QLabel("Item ID cannot be changed")
            layout.addWidget(note)

        value_layout = QHBoxLayout()
        value_layout.addWidget(QLabel("Sell Value:"))
        self.value_input = QSpinBox()
        self.value_input.setMinimum(0)
        self.value_input.setMaximum(1_000_000_000)
        self.value_input.setValue(default_value)
        value_layout.addWidget(self.value_input)
        layout.addLayout(value_layout)

        btn_layout = QHBoxLayout()
        ok_btn = QPushButton("OK")
        ok_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(ok_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)


        self.setLayout(layout)

        if not editing:
            self.update_id_field()

    def update_id_field(self):
        if not self.editing:
            self.id_input.setText(slugify(self.name_input.text()))
    
    def get_data(self):
        return self.name_input.text(), self.id_input.text(), self.value_input.value()

def slugify(text: str) ->str:
    return text.lower().replace(" ", "_")
