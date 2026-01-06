import sys
from Item import Item
from Recipe import Recipe
from CraftingDatabase import CraftingDatabase
from PySide6.QtWidgets import QCompleter, QComboBox, QFormLayout, QSpinBox, QLineEdit, QDialog, QMessageBox, QInputDialog, QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QLabel, QTabWidget, QListWidget, QHBoxLayout
from PySide6.QtCore import Qt, Signal, QTimer, QEvent

class RecipeDialog(QDialog):
    def __init__(self, items: dict[str, Item], recipe = None, parent=None, title="Add Recipe"):
        super().__init__(parent)
        self.setWindowTitle(title)

        self.items = items
        self.recipe = recipe

       

        main_layout = QVBoxLayout(self)


        main_layout.addWidget(QLabel("Inputs"))

        self.inputs_layout = QVBoxLayout()
        main_layout.addLayout(self.inputs_layout)

        self.add_input_btn = QPushButton("+ Add Input")
        main_layout.addWidget(self.add_input_btn)
        self.add_input_btn.clicked.connect(self.add_input_row)
        self.input_rows = []

        main_layout.addWidget(QLabel("Outputs"))

        self.outputs_layout = QVBoxLayout()
        main_layout.addLayout(self.outputs_layout)

        self.add_outputs_btn = QPushButton("+ Add Output")
        main_layout.addWidget(self.add_outputs_btn)
        self.add_outputs_btn.clicked.connect(self.add_output_row)
        self.output_rows = []

        form = QFormLayout()
        self.type_edit = QLineEdit("CRAFT")
        self.time_spin = QSpinBox()
        self.time_spin.setMinimum(0)

        form.addRow("Type:", self.type_edit)
        form.addRow("Time:", self.time_spin)

        main_layout.addLayout(form)

        btn_layout = QHBoxLayout()
        self.save_btn = QPushButton("Save")
        self.cancel_btn = QPushButton("Cancel")

        btn_layout.addStretch()
        btn_layout.addWidget(self.save_btn)
        btn_layout.addWidget(self.cancel_btn)

        main_layout.addLayout(btn_layout)

        self.save_btn.clicked.connect(self.on_save)
        self.cancel_btn.clicked.connect(self.reject)

        if self.recipe:
            self.populate_from_recipe()


    def add_input_row(self):
        row = IngredientRow(self.items)
        row.remove_requested.connect(self.remove_input_row)
        self.inputs_layout.addWidget(row)
        self.input_rows.append(row)
        return row
    
    def add_output_row(self):
        row = IngredientRow(self.items)
        row.remove_requested.connect(self.remove_output_row)
        self.outputs_layout.addWidget(row)
        self.output_rows.append(row)
        return row

    def remove_input_row(self, row:IngredientRow):
        if row in self.input_rows:
            self.input_rows.remove(row)
            row.setParent(None)
            row.deleteLater()

    def remove_output_row(self, row):
        if row in self.output_rows:
            self.output_rows.remove(row)
            row.setParent(None)
            row.deleteLater()
    
    def populate_from_recipe(self):
        if not self.recipe:
            return
        
        for item_id, qty in self.recipe.inputs.items():
            row = self.add_input_row()
            row.item_combo.setCurrentIndex(row.item_combo.findData(item_id))
            row.qty_spin.setValue(qty)

        for item_id, qty in self.recipe.outputs.items():
            row = self.add_output_row()
            row.item_combo.setCurrentIndex(row.item_combo.findData(item_id))
            row.qty_spin.setValue(qty)

        self.type_edit.setText(self.recipe.type)
        self.time_spin.setValue(int(self.recipe.time))


    def on_save(self):
        inputs = {}
        row:IngredientRow
        for row in self.input_rows:
            item_id = row.item_combo.currentData()
            quantity = row.qty_spin.value()

            if not item_id:
                QMessageBox.warning (self, "Invalid input", "All input rows must have an item selected.")
                return
            if quantity <= 0:
                QMessageBox.warning(self, "Invalid input", f"Quantity for item '{item_id}' must be positive")
                return
            if item_id in inputs:
                QMessageBox.warning(self, "Duplicate input", f"Item '{item_id}' appears more than once in inputs")
                return
            inputs[item_id] = quantity

        outputs = {}
        row:IngredientRow
        for row in self.output_rows:
            item_id = row.item_combo.currentData()
            quantity = row.qty_spin.value()

            if not item_id:
                QMessageBox.warning (self, "Invalid input", "All output rows must have an item selected.")
                return
            if quantity <= 0:
                QMessageBox.warning(self, "Invalid input", f"Quantity for item '{item_id}' must be positive")
                return
            if item_id in outputs:
                QMessageBox.warning(self, "Duplicate input", f"Item '{item_id}' appears more than once in outputs")
                return
            outputs[item_id] = quantity
        
        if not inputs or not outputs:
            QMessageBox.warning(self, "Invalid recipe", "A recipe must have at least one input and one output.")
            return

        recipe_type = self.type_edit.text()
        recipe_time = self.time_spin.value()

        try:
            recipe = Recipe(inputs, outputs, type=recipe_type, time=recipe_time)
        except Exception as e:
            QMessageBox.warning(self, "Invalid recipe", str(e))
            return

        self.recipe = recipe
        self.accept()

class IngredientRow(QWidget):
    
    remove_requested = Signal(object)

    def __init__(self, items: dict[str, Item], parent=None):
        super().__init__(parent)

        self.items = items

        layout = QHBoxLayout(self)

        self.item_combo = QComboBox()
        self.item_combo.setEditable(True)
        self.item_combo.setInsertPolicy(QComboBox.NoInsert)
        self.item_combo.completer().setCompletionMode(QCompleter.PopupCompletion)
        self.item_combo.completer().setFilterMode(Qt.MatchContains)
        self.item_combo.addItem("Select item...", None)
        self.line_edit = self.item_combo.lineEdit()
        self.line_edit.installEventFilter(self)


        for item_id, item in sorted(items.items(), key=lambda kv: kv[1].name.lower()):
            self.item_combo.addItem(item.name, item_id)



        self.qty_spin = QSpinBox()
        self.qty_spin.setMinimum(1)
        self.qty_spin.setMaximum(1_000_000_000)
        self.qty_spin.setValue(1)

        self.remove_btn = QPushButton("X")
        self.remove_btn.setFixedWidth(28)

        layout.addWidget(self.item_combo)
        layout.addWidget(self.qty_spin)
        layout.addWidget(self.remove_btn)

        QTimer.singleShot(0, lambda: self._focus_combo())

        self.remove_btn.clicked.connect(self.on_remove)
    
    def _focus_combo(self):
        self.item_combo.setFocus()
        self.item_combo.lineEdit().selectAll()

    def eventFilter(self, obj, event):
        if obj == self.item_combo.lineEdit():
            if event.type() ==QEvent.MouseButtonPress:
                QTimer.singleShot(0, obj.selectAll)
        return super().eventFilter(obj, event)

    def on_remove(self):
        self.remove_requested.emit(self)