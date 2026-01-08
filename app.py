import sys
from Item import Item
from Recipe import Recipe
from CraftingDatabase import CraftingDatabase
from ItemDialog import ItemDialog
from RecipeDialog import RecipeDialog, IngredientRow
from PySide6.QtWidgets import QComboBox, QLineEdit, QFileDialog, QListWidgetItem, QDialog, QMessageBox, QInputDialog, QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QLabel, QTabWidget, QListWidget, QHBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QBrush

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.db = CraftingDatabase()

        self.setWindowTitle("Crafting Database GUI")
        self.resize(600, 400)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.build_items_tab()
        self.build_recipes_tab()
        self.build_options_tab()
        self.wire_signals()
        
        
    def build_items_tab(self):
        self.items_tab = QWidget()
        self.items_layout = QVBoxLayout()
        self.items_tab.setLayout(self.items_layout)
        self.items_layout.addWidget(QLabel("Items will appear here"))
        self.tabs.addTab(self.items_tab, "Items")

        self.items_label = QLabel("Items")
        self.items_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.items_layout.addWidget(self.items_label)

        self.items_list = QListWidget()
        self.items_layout.addWidget(self.items_list)

        self.items_buttons = QHBoxLayout()
        self.items_add = QPushButton("Add")
        self.items_edit = QPushButton("Edit")
        self.items_remove = QPushButton("Remove")
        self.items_buttons.addWidget(self.items_add)
        self.items_buttons.addWidget(self.items_edit)
        self.items_buttons.addWidget(self.items_remove)
        self.items_layout.addLayout(self.items_buttons)

    def build_recipes_tab(self):
        self.recipes_tab = QWidget()
        self.recipes_layout = QVBoxLayout()
        self.recipes_tab.setLayout(self.recipes_layout)
        self.recipes_layout.addWidget(QLabel("Recipes will appear here"))
        self.tabs.addTab(self.recipes_tab, "Recipes")

        self.recipes_label = QLabel("Recipes")
        self.recipes_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.recipes_layout.addWidget(self.recipes_label)


        self.recipe_sort_layout = QHBoxLayout()
        self.recipe_sort_label = QLabel("Sort by:")
        self.recipe_sort_combo = QComboBox()
        self.recipe_sort_combo.addItems(["Profit", "Time", "Type", "Inputs","Outputs"])
        self.recipe_sort_dir = QComboBox()
        self.recipe_sort_dir.addItems(["Descending", "Ascending"])
        self.recipe_sort_layout.addWidget(self.recipe_sort_label)
        self.recipe_sort_layout.addWidget(self.recipe_sort_combo)
        self.recipe_sort_layout.addWidget(self.recipe_sort_dir)
        self.recipe_sort_layout.addStretch()
        self.recipes_layout.addLayout(self.recipe_sort_layout)

        self.recipe_sort_combo.currentIndexChanged.connect(self.refresh_recipes_list)
        self.recipe_sort_dir.currentIndexChanged.connect(self.refresh_recipes_list)


        self.recipes_list = QListWidget()
        self.recipes_layout.addWidget(self.recipes_list)

        self.recipes_buttons = QHBoxLayout()
        self.recipes_add = QPushButton("Add")
        self.recipes_edit = QPushButton("Edit")
        self.recipes_remove = QPushButton("Remove")
        self.recipes_buttons.addWidget(self.recipes_add)
        self.recipes_buttons.addWidget(self.recipes_edit)
        self.recipes_buttons.addWidget(self.recipes_remove)
        self.recipes_layout.addLayout(self.recipes_buttons)

    def build_options_tab(self):

        self.options_tab = QWidget()
        self.options_layout = QVBoxLayout()
        self.options_tab.setLayout(self.options_layout)
        self.tabs.addTab(self.options_tab, "Options")

        self.options_label = QLabel("Database Options")
        self.options_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.options_layout.addWidget(self.options_label)

        self.name_layout = QHBoxLayout()
        self.name_layout.addWidget(QLabel("Database name"))

        self.db_name_edit = QLineEdit()
        self.db_name_edit.setText(self.db.name)
        self.name_layout.addWidget(self.db_name_edit)

        self.options_layout.addLayout(self.name_layout)

        self.save_db_btn = QPushButton("Save database to file")
        self.load_db_btn = QPushButton("Load database from file")
        self.options_layout.addWidget(self.save_db_btn)
        self.options_layout.addWidget(self.load_db_btn)

        self.options_layout.addStretch()

    def wire_signals(self):
        
        self.items_add.clicked.connect(self.add_item)
        self.items_edit.clicked.connect(self.edit_item)
        self.items_remove.clicked.connect(self.remove_item)

        self.recipes_add.clicked.connect(self.add_recipe)
        self.recipes_edit.clicked.connect(self.edit_recipe)
        self.recipes_remove.clicked.connect(self.remove_recipe)
   
        self.save_db_btn.clicked.connect(self.save_database)
        self.load_db_btn.clicked.connect(self.load_database)
        self.db_name_edit.textChanged.connect(self.on_db_name_changed)

    def add_item(self):
        dialog = ItemDialog(parent=self)
        if dialog.exec():
            name, item_id, sell_value = dialog.get_data()
            success, msg = self.db.add_item(Item(item_id, name, sell_value))
            QMessageBox.information(self, "Add Item", msg)
            if success:
                self.refresh_items_list()

    def edit_item(self):
        selected = self.items_list.currentRow()
        if selected < 0:
            print("No item selected")
            return

        
        item_id = self.items_list.item(selected).data(Qt.UserRole)
        item = self.db.items[item_id]

        # Open dialog in editing mode
        dialog = ItemDialog(
            self, 
            title="Edit Item", 
            default_name=item.name, 
            default_id=item.id, 
            default_value=item.sell_value, 
            editing=True
        )

        if dialog.exec():
            new_name, _, new_value = dialog.get_data()
            self.db.edit_item(item_id, new_name=new_name, new_sell_value=new_value)
            self.refresh_items_list()

    def remove_item(self):
        selected = self.items_list.currentRow()
        if selected < 0:
            print("No item selected")
            return
        

        success, msg = self.db.remove_item(self.items_list.item(selected).data(Qt.UserRole))

        if not success:
            reply = QMessageBox.question(
                self,
                "Item in recipes",
                f"{msg}\nDo you want to remove the item and all its recipes?",
                QMessageBox.Yes | QMessageBox.No
            )
        
            if reply == QMessageBox.Yes:
                success, msg = self.db.remove_item(self.items_list.item(selected).data(Qt.UserRole), cascade=True)
            else:
                return
            
        if success:
            QMessageBox.information(self, "Success", msg)
            self.refresh_items_list()
            self.refresh_recipes_list()
        else:
            QMessageBox.warning(self,"Error", msg)

    def add_recipe(self):
        dialog = RecipeDialog(self.db.items, parent=self)
        if dialog.exec() == QDialog.Accepted:
            success, msg = self.db.add_recipe(dialog.recipe)
            QMessageBox.information(self, "Add Recipe", msg)
            self.refresh_recipes_list()
            
    def edit_recipe(self):
        selected = self.recipes_list.currentRow()
        if selected < 0:
            print("No recipe selected")
            return

        recipe = self.recipes_list.item(selected).data(Qt.UserRole)
        dialog = RecipeDialog(self.db.items, recipe=recipe, parent=self, title="Edit Recipe")
        
        if dialog.exec() == QDialog.Accepted:
            new_recipe = dialog.recipe
            success, msg = self.db.edit_recipe(recipe, new_recipe)
            QMessageBox.information(self, "Edit Recipe", msg)
            self.refresh_recipes_list()

    def remove_recipe(self):
        selected = self.recipes_list.currentRow()
        if selected < 0:
            print("No recipe selected")
            return

        success, msg = self.db.remove_recipe(self.recipes_list.item(selected).data(Qt.UserRole))
        if success:
            QMessageBox.information(self, "Remove Recipe", msg)
            self.refresh_recipes_list()
        else:
            QMessageBox.warning(self, "Error", msg)

    def refresh_items_list(self):
        self.items_list.clear()
        for i in self.db.items.values():
            list_item = QListWidgetItem(f"{i.name} (${i.sell_value})")
            list_item.setData(Qt.UserRole, i.id)
            self.items_list.addItem(list_item)
        self.items_list.sortItems()
        
    def refresh_recipes_list(self):
    
        self.recipes_list.clear()
        for r in self.get_sorted_recipes():
            text = str(r)
            profit = self.db.calc_profit(r)[1]

            item = self.create_recipe_list_item(r)
            item.setData(Qt.UserRole, r)

            self.recipes_list.addItem(item)

    def create_recipe_list_item(self, recipe):
        
        
        # Format inputs and outputs
        inputs_str = ", ".join(f"{qty}x {self.db.items[i].name}" for i, qty in sorted(recipe.inputs.items()))
        outputs_str = ", ".join(f"{qty}x {self.db.items[i].name}" for i, qty in sorted(recipe.outputs.items()))

        # Type and time
        type_str = recipe.type
        time_str = f"{recipe.time}s"

        # Profit
        success, profit = self.db.calc_profit(recipe)
        profit_str = f"Profit: {profit}" if success else "Profit: N/A"

        # Full display text
        display_text = f"{type_str}: {inputs_str} → {outputs_str} | {time_str} | {profit_str}"
       
        # Create the item
        list_item = QListWidgetItem(display_text)
        list_item.setData(Qt.UserRole, recipe)

        # Partial coloring using QBrush — approximate, applies to whole item for now
        # Green outputs, red inputs, black for rest (we can only color the whole item in QListWidget without using delegates)
        if success:
            if profit > 0:
                list_item.setForeground(QBrush(QColor("green")))
            elif profit < 0:
                list_item.setForeground(QBrush(QColor("red")))
            else:
                list_item.setForeground(QBrush(QColor("black")))

        return list_item

    def get_sorted_recipes(self):
        recipes = list(self.db.recipes)

        key = self.recipe_sort_combo.currentText()
        descending = self.recipe_sort_dir.currentText() == "Descending"

        if key == "Profit":
            recipes.sort(key=lambda r: self.db.calc_profit(r), reverse=descending)
        if key == "Time":
            recipes.sort(key=lambda r: r.time, reverse=descending)
        if key == "Type":
            recipes.sort(key=lambda r: r.time, reverse=descending)
        if key == "Inputs":
            recipes.sort(key=lambda r: ", ".join(self.db.items[i].name for i in sorted(r.inputs)), reverse=descending)
        if key == "Outputs":
            recipes.sort(key=lambda r: ", ".join(self.db.items[i].name for i in sorted(r.outputs)), reverse=descending)

        return recipes

    def save_database(self):
        default = self.db.name or "crafting_database"
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Save Database",
            f"{default}.json",
            "JSON Files (*.json)"
        )
        
        if not filename:
            return
    
        try:
            self.db.save(filename)
            QMessageBox.information(self, "Save Database", f"Database saved as '{filename}'")
        except Exception as e:
            QMessageBox.critical(self, "Save Error", str(e))
    
    def load_database(self):
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Load Database,",
            "",
            "JSON Files (*.json)"
        )

        if not filename:
            return
        
        try:
            self.db = CraftingDatabase.load(filename)
            self.db_name_edit.setText(self.db.name)
            QMessageBox.information(self, "Load Database", f"Database loaded from '{filename}'")
            self.refresh_items_list()
            self.refresh_recipes_list()
        except FileNotFoundError:
            QMessageBox.warning(self, "Load Error", f"File '{filename}' not found")
        except Exception as e:
            QMessageBox.critical(self, "Load Error", str(e))

    def on_db_name_changed(self, text):
        self.db.name = text.strip()

app = QApplication(sys.argv)

window = MainWindow()
window.show()

sys.exit(app.exec())