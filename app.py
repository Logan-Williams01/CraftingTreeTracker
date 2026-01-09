import sys
from Item import Item
from Recipe import Recipe
from CraftingDatabase import CraftingDatabase
from ItemDialog import ItemDialog
from RecipeDialog import RecipeDialog, IngredientRow
from PySide6.QtWidgets import QSizePolicy, QComboBox, QLineEdit, QFileDialog, QListWidgetItem, QDialog, QMessageBox, QInputDialog, QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QLabel, QTabWidget, QListWidget, QHBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QBrush

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Main Database
        self.db = CraftingDatabase()

        #Main window title and default size
        self.setWindowTitle("Crafting Database GUI")
        self.resize(600, 400)

        # Main window is broken into tabs at the top of application
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Build tabs in separate methods, not chaotically in __init__
        self.build_items_tab()
        self.build_recipes_tab()
        self.build_options_tab()
        self.wire_signals()
        
    def build_items_tab(self):

        # Create tab and layout and add self to main tabs widget
        self.items_tab = QWidget()
        self.items_layout = QVBoxLayout()
        self.items_tab.setLayout(self.items_layout)
        self.tabs.addTab(self.items_tab, "Items")

        # Central items label
        self.items_label = QLabel("Items")
        self.items_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.items_layout.addWidget(self.items_label)

        # Sorting line with criteria and direction
        self.item_sort_layout = QHBoxLayout()
        self.items_layout.addLayout(self.item_sort_layout)

        # Label
        self.item_sort_label = QLabel("Sort by:")
        self.item_sort_layout.addWidget(self.item_sort_label)

        # Criteria with set width/height
        self.item_sort_combo = QComboBox()
        self.item_sort_combo.addItems(["Name", "Value"])
        self.item_sort_combo.setFixedWidth(90)
        self.item_sort_combo.setFixedHeight(25)
        self.item_sort_layout.addWidget(self.item_sort_combo)

        # Direction with set width/height
        self.item_sort_dir = QComboBox()
        self.item_sort_dir.addItems(["Ascending", "Descending"])
        self.item_sort_dir.setFixedWidth(90)
        self.item_sort_dir.setFixedHeight(25)
        self.item_sort_layout.addWidget(self.item_sort_dir)
        
        # Keep the buttons in place
        self.item_sort_layout.addStretch()
        
        # Add the Items list
        self.items_list = QListWidget()
        self.items_layout.addWidget(self.items_list)

        # Add the buttons below for adding/editing/removing items
        self.items_buttons = QHBoxLayout()
        self.items_add = QPushButton("Add")
        self.items_edit = QPushButton("Edit")
        self.items_remove = QPushButton("Remove")
        self.items_buttons.addWidget(self.items_add)
        self.items_buttons.addWidget(self.items_edit)
        self.items_buttons.addWidget(self.items_remove)
        self.items_layout.addLayout(self.items_buttons)

    def build_recipes_tab(self):
       
        # Create tab and layout and add self to main tabs widget
        self.recipes_tab = QWidget()
        self.recipes_layout = QVBoxLayout()
        self.recipes_tab.setLayout(self.recipes_layout)
        self.tabs.addTab(self.recipes_tab, "Recipes")

        # Central recipes layout
        self.recipes_label = QLabel("Recipes")
        self.recipes_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.recipes_layout.addWidget(self.recipes_label)

        # Sorting line with criteria and direction
        self.recipe_sort_layout = QHBoxLayout()
        self.recipes_layout.addLayout(self.recipe_sort_layout)

        # Label
        self.recipe_sort_label = QLabel("Sort by:")
        self.recipe_sort_layout.addWidget(self.recipe_sort_label)

        # Criteria with set width/height
        self.recipe_sort_combo = QComboBox()
        self.recipe_sort_combo.addItems(["Profit", "Time", "Type", "Inputs","Outputs"])
        self.recipe_sort_combo.setFixedWidth(90)
        self.recipe_sort_combo.setFixedHeight(25)
        self.recipe_sort_layout.addWidget(self.recipe_sort_combo)        

        # Direction with set width/height
        self.recipe_sort_dir = QComboBox()
        self.recipe_sort_dir.addItems(["Ascending", "Descending"])
        self.recipe_sort_dir.setFixedWidth(90)
        self.recipe_sort_dir.setFixedHeight(25)
        self.recipe_sort_layout.addWidget(self.recipe_sort_dir)

        # Add to keep the buttons in place
        self.recipe_sort_layout.addStretch()
           
        # Filtering line with Item selector and Input/Output selector, and Clear button to unfilter
        self.recipe_filter_layout = QHBoxLayout()
        self.recipes_layout.addLayout(self.recipe_filter_layout)

        # Label
        self.recipe_filter_label = QLabel("Filter by:")
        self.recipe_filter_layout.addWidget(self.recipe_filter_label)        
        
        # Item selector using a modified IngredientRow to only select existing items
        self.recipe_filter_item = IngredientRow(self.db.items, parent=self)
        self.recipe_filter_item.qty_spin.deleteLater()
        self.recipe_filter_item.remove_btn.deleteLater()
        self.recipe_filter_item.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.recipe_filter_layout.addWidget(self.recipe_filter_item)

        # Input/Output Selector
        self.recipe_filter_type = QComboBox()
        self.recipe_filter_type.addItems(["Both", "Inputs", "Outputs"])
        self.recipe_filter_type.setFixedWidth(90)
        self.recipe_filter_type.setFixedHeight(25)
        self.recipe_filter_layout.addWidget(self.recipe_filter_type)

        # Clear button
        self.recipe_filter_clear_btn = QPushButton("Clear")
        self.recipe_filter_clear_btn.setFixedWidth(90)
        self.recipe_filter_clear_btn.setFixedHeight(25)
        self.recipe_filter_layout.addWidget(self.recipe_filter_clear_btn)

        # Add the Recipe list
        self.recipes_list = QListWidget()
        self.recipes_layout.addWidget(self.recipes_list)

        # Add the buttons below for adding/editing/removing recipes
        self.recipes_buttons = QHBoxLayout()
        self.recipes_add = QPushButton("Add")
        self.recipes_edit = QPushButton("Edit")
        self.recipes_remove = QPushButton("Remove")
        self.recipes_buttons.addWidget(self.recipes_add)
        self.recipes_buttons.addWidget(self.recipes_edit)
        self.recipes_buttons.addWidget(self.recipes_remove)
        self.recipes_layout.addLayout(self.recipes_buttons)

    def build_options_tab(self):

        # Create tab and layout and add self to main tabs widget
        self.options_tab = QWidget()
        self.options_layout = QVBoxLayout()
        self.options_tab.setLayout(self.options_layout)
        self.tabs.addTab(self.options_tab, "Options")

        # Central label
        self.options_label = QLabel("Database Options")
        self.options_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.options_layout.addWidget(self.options_label)

        # Database name label
        self.name_layout = QHBoxLayout()
        self.name_layout.addWidget(QLabel("Database name"))

        # Database name editor
        self.db_name_edit = QLineEdit()
        self.db_name_edit.setText(self.db.name)
        self.name_layout.addWidget(self.db_name_edit)
        self.options_layout.addLayout(self.name_layout)

        # Save and Load buttons
        self.save_db_btn = QPushButton("Save database to file")
        self.load_db_btn = QPushButton("Load database from file")
        self.options_layout.addWidget(self.save_db_btn)
        self.options_layout.addWidget(self.load_db_btn)

        # Keep buttons in place
        self.options_layout.addStretch()

    def wire_signals(self):
        
        # Item sort options auto-refresh
        self.item_sort_combo.currentIndexChanged.connect(self.refresh_items_list)
        self.item_sort_dir.currentIndexChanged.connect(self.refresh_items_list)

        # Double click an Item to instantly see it's Recipes
        self.items_list.itemDoubleClicked.connect(self.go_to_recipe)

        # Item add/edit/remove buttons
        self.items_add.clicked.connect(self.add_item)
        self.items_edit.clicked.connect(self.edit_item)
        self.items_remove.clicked.connect(self.remove_item)

        # Recipe sort options auto-refresh
        self.recipe_sort_combo.currentIndexChanged.connect(self.refresh_recipes_list)
        self.recipe_sort_dir.currentIndexChanged.connect(self.refresh_recipes_list)

        # Recipe filter options auto-refresh
        self.recipe_filter_item.item_combo.currentIndexChanged.connect(self.refresh_recipes_list)
        self.recipe_filter_type.currentIndexChanged.connect(self.refresh_recipes_list)
        self.recipe_filter_clear_btn.clicked.connect(self.clear_recipe_filter)
       
        # Recipe add/edit/remove buttons
        self.recipes_add.clicked.connect(self.add_recipe)
        self.recipes_edit.clicked.connect(self.edit_recipe)
        self.recipes_remove.clicked.connect(self.remove_recipe)
   
        # Options database name changer
        self.db_name_edit.textChanged.connect(self.on_db_name_changed)

        # Options Save/Load buttons
        self.save_db_btn.clicked.connect(self.save_database)
        self.load_db_btn.clicked.connect(self.load_database)
        
    def add_item(self):

        # Create a window for editing Item params
        dialog = ItemDialog(parent=self)
        
        # If the dialog window runs successfully
        if dialog.exec() == QDialog.Accepted:

            name, item_id, sell_value = dialog.get_data()

            # Attempts to add the item to the database using the Item constructor
            success, msg = self.db.add_item(Item(item_id, name, sell_value))

            # Small window saying the item was added
            QMessageBox.information(self, "Add Item", msg)

            # If item was added, refresh the item list
            if success:
                self.refresh_items_list()

    def edit_item(self):

        # Get current selected item, abort if no item selected
        selected = self.items_list.currentRow()
        if selected < 0:
            print("No item selected")
            return

        # Items are stored in Qt.UserRole
        item = self.items_list.item(selected).data(Qt.UserRole)
        item_id = item.id

        # Create a window for editing item params, but preloaded with existing values
        dialog = ItemDialog(
            self, 
            title="Edit Item", 
            default_name=item.name, 
            default_id=item.id, 
            default_value=item.sell_value, 
            editing=True
        )

        # If the dialog window runs successfully
        if dialog.exec() == QDialog.Accepted:

            #Item id's can't be changed, so _id is left unused
            new_name, _id, new_value = dialog.get_data()
            success, msg = self.db.edit_item(item_id, new_name=new_name, new_sell_value=new_value)

            # Small window saying the item was edited
            QMessageBox.information(self, "Add Item", msg)
            
            # If item was edited, refresh the item list
            if success:
                self.refresh_items_list()

    def remove_item(self):

        # Get current selected item, abort if no item selected
        selected = self.items_list.currentRow()
        if selected < 0:
            print("No item selected")
            return
        
        # Since Recipes rely on their inputs/outputs actually existing, only Items not used in Recipes may be removed

        # Attempt to remove the item without cascading (removing related Recipes)
        success, msg = self.db.remove_item(self.items_list.item(selected).data(Qt.UserRole).id, cascade=False)

        # Item exists in at least one recipe
        if not success:

            #Give a window explaining the problem
            reply = QMessageBox.question(
                self,
                "Item in recipes",
                f"{msg}\nDo you want to remove the item and all its recipes?",
                QMessageBox.Yes | QMessageBox.No
            )
        
            # User selected yes, remove all Item's recipes and the Item itself
            if reply == QMessageBox.Yes:
                success, msg = self.db.remove_item(self.items_list.item(selected).data(Qt.UserRole).id, cascade=True)
            else:
                return
            
        # If successful, refresh both the Items list, and the Recipes list (incase recipes were removed)
        if success:
            QMessageBox.information(self, "Success", msg)
            self.refresh_items_list()
            self.refresh_recipes_list()
        else:
            QMessageBox.warning(self,"Error", msg)

    def go_to_recipe(self, item_widget):
        
        # Loop through items in recipe tab's items an look for matching data, then set to current index
        for i in range(self.recipe_filter_item.item_combo.count()):
           
           if item_widget.data(Qt.UserRole).id == self.recipe_filter_item.item_combo.itemData(i):
               self.recipe_filter_item.item_combo.setCurrentIndex(i)
               break
            
        
        
        self.tabs.setCurrentWidget(self.recipes_tab)

    def add_recipe(self):

        # Create a window for editing Recipe params
        dialog = RecipeDialog(self.db.items, parent=self)

        # If the Dialog runs successfully
        if dialog.exec() == QDialog.Accepted:
            
            # Recipe creation is more complex, so the dialog handles it entirely
            success, msg = self.db.add_recipe(dialog.recipe)
            QMessageBox.information(self, "Add Recipe", msg)

            # If successful, refresh the recipe list
            if success:
                self.refresh_recipes_list()
            
    def edit_recipe(self):

        # Get currently selected Recipe, abort if no Recipe selected
        selected = self.recipes_list.currentRow()
        if selected < 0:
            print("No recipe selected")
            return

        # Recipe is stored in UserRole
        recipe = self.recipes_list.item(selected).data(Qt.UserRole)

        # Create a window for editing Recipe params, but preloaded with existing values
        dialog = RecipeDialog(self.db.items, recipe=recipe, parent=self, title="Edit Recipe")
        
        #If the dialog runs successfully
        if dialog.exec() == QDialog.Accepted:
            new_recipe = dialog.recipe
            success, msg = self.db.edit_recipe(recipe, new_recipe)
            QMessageBox.information(self, "Edit Recipe", msg)

            # If successful, refresh recipe list
            if success:
                self.refresh_recipes_list()

    def remove_recipe(self):

        #Get currently selected Recipe, abort if no Recipe selected
        selected = self.recipes_list.currentRow()
        if selected < 0:
            print("No recipe selected")
            return

        # Remove Recipe, no additional logic required like with Items
        success, msg = self.db.remove_recipe(self.recipes_list.item(selected).data(Qt.UserRole))
        
        # If successful, refresh Recipe list
        if success:
            QMessageBox.information(self, "Remove Recipe", msg)
            self.refresh_recipes_list()
        else:
            QMessageBox.warning(self, "Error", msg)

    def refresh_items_list(self):
        
        # Clear the items list
        self.items_list.clear()

        # Gets current items in list of tuples
        for i in self.get_sorted_items():

            # Format item display name
            list_item = QListWidgetItem(f"{i[1].name} (${i[1].sell_value})")

            # Set UserRole to the Item obj itself
            list_item.setData(Qt.UserRole, i[1])

            # Add item to list widget
            self.items_list.addItem(list_item)
        
        # Also update the list of items in the recipe tab's item drop-down (the modified IngredientRow), to ensure they stay synced
        self.recipe_filter_item.refresh_items(self.db.items)
        
    def get_sorted_items(self):

        # Pull the current dictionary of items
        items = self.db.items

        # Direction flag
        descending = self.item_sort_dir.currentText() == "Descending"

        # Get a list of tuples, converted from dictionaries by sorted()
        # Sorted by either name or sell_value
        if self.item_sort_combo.currentText() == "Name":
            sorted_items = sorted(items.items(), key=lambda item: item[1].name.lower(), reverse=descending)
        elif self.item_sort_combo.currentText() == "Value":
            sorted_items = sorted(items.items(), key=lambda item: item[1].sell_value, reverse=descending)
        
        return sorted_items

    def refresh_recipes_list(self):
    
        # Clear the recipes list
        self.recipes_list.clear()

        # Grab both the item to filter by and whether to use Inputs/Outputs/Both
        item_filter = self.recipe_filter_item.item_combo
        type_filter = self.recipe_filter_type

        # Get current Recipes in a list of Recipe objects
        for r in self.get_sorted_recipes():
           
            # Formats and colors the Recipe into a string to insert into the list widget
            item = self.create_recipe_list_item(r)

            # Stores the Recipe onj itself into UserRole
            item.setData(Qt.UserRole, r)
            
            # If the item filter has no data, do not filter items
            # Otherwise, use Recipe's consumes() and produces() with the item_filter's current item to determine if it gets added
            if not item_filter.currentData():
                self.recipes_list.addItem(item)
            elif type_filter.currentText() == "Both":
                if r.consumes(item_filter.currentData()) or r.produces(item_filter.currentData()):
                    self.recipes_list.addItem(item)
            elif type_filter.currentText() == "Inputs":
                if r.consumes(item_filter.currentData()):
                    self.recipes_list.addItem(item)
            elif type_filter.currentText() == "Outputs":
                if r.produces(item_filter.currentData()):
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
       
        # Create the widget
        list_item = QListWidgetItem(display_text)
        list_item.setData(Qt.UserRole, recipe)

        # Coloring using QBrush, based on the total sell_values of the inputs and outputs
        # Green is profitable, red is a net loss, black is break-even
        if success:
            if profit > 0:
                list_item.setForeground(QBrush(QColor("green")))
            elif profit < 0:
                list_item.setForeground(QBrush(QColor("red")))
            else:
                list_item.setForeground(QBrush(QColor("black")))

        return list_item

    def get_sorted_recipes(self):
        
        # Grab current Recipes
        recipes = list(self.db.recipes)

        # Grab current sort criteria and direction
        key = self.recipe_sort_combo.currentText()
        descending = self.recipe_sort_dir.currentText() == "Descending"

        # Sort based on key and direction using built-in .sort()
        if key == "Profit":
            recipes.sort(key=lambda r: self.db.calc_profit(r), reverse=descending)
        if key == "Time":
            recipes.sort(key=lambda r: r.time, reverse=descending)
        if key == "Type":
            recipes.sort(key=lambda r: r.type, reverse=descending)
        if key == "Inputs":
            recipes.sort(key=lambda r: ", ".join(self.db.items[i].name for i in sorted(r.inputs)), reverse=descending)
        if key == "Outputs":
            recipes.sort(key=lambda r: ", ".join(self.db.items[i].name for i in sorted(r.outputs)), reverse=descending)

        return recipes

    def clear_recipe_filter(self):

        # Easy button for removing current filter
        self.recipe_filter_item.item_combo.setCurrentIndex(0)
        self.recipe_filter_type.setCurrentIndex(0)

    def save_database(self):

        # Get database's name or default
        default = self.db.name or "crafting_database"

        # Open a window for file explorer
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Save Database",
            f"{default}.json",
            "JSON Files (*.json)"
        )
        
        # Don't save empty filename
        if not filename:
            return
    
        # Run database's save() method and display a window saying whether it succeeded
        try:
            self.db.save(filename)
            QMessageBox.information(self, "Save Database", f"Database saved as '{filename}'")
        except Exception as e:
            QMessageBox.critical(self, "Save Error", str(e))
    
    def load_database(self):

        # Open a window for file explorer
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Load Database,",
            "",
            "JSON Files (*.json)"
        )

        # Don't open an empty filename
        if not filename:
            return
        
        # Run CraftingDatabase's load() method to create a database, set it's name, and refresh the Item and Recipe lists and display a window saying whether it succeeded
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

        # Change database's name
        self.db.name = text.strip()

# Make stuff run
app = QApplication(sys.argv)

window = MainWindow()
window.show()

sys.exit(app.exec())