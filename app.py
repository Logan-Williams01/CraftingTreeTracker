import sys
from Item import Item
from Recipe import Recipe
from CraftingDatabase import CraftingDatabase
from ItemDialog import ItemDialog
from RecipeDialog import RecipeDialog, IngredientRow
from PySide6.QtWidgets import QListWidgetItem, QDialog, QMessageBox, QInputDialog, QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QLabel, QTabWidget, QListWidget, QHBoxLayout
from PySide6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.db = CraftingDatabase()

        self.setWindowTitle("Crafting Database GUI")
        self.resize(600, 400)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

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

        self.items_add.clicked.connect(self.add_item)
        self.items_edit.clicked.connect(self.edit_item)
        self.items_remove.clicked.connect(self.remove_item)


        self.recipes_tab = QWidget()
        self.recipes_layout = QVBoxLayout()
        self.recipes_tab.setLayout(self.recipes_layout)
        self.recipes_layout.addWidget(QLabel("Recipes will appear here"))
        self.tabs.addTab(self.recipes_tab, "Recipes")

        self.recipes_label = QLabel("Recipes")
        self.recipes_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.recipes_layout.addWidget(self.recipes_label)

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

        self.recipes_add.clicked.connect(self.add_recipe)
        self.recipes_edit.clicked.connect(self.edit_recipe)
        self.recipes_remove.clicked.connect(self.remove_recipe)

        self.label = QLabel("Hello, Crafting Database!")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        #self.setCentralWidget(label)
    
    def add_item(self):
        dialog = ItemDialog(parent=self)
        if dialog.exec():
            name, item_id, sell_value = dialog.get_data()
            success, msg = self.db.add_item(Item(item_id, name, sell_value))
            print(msg)
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
        
        
        # Get the item ID from the list text
        list_text = self.items_list.item(selected).text()
        item_id = list_text.split("(")[1].split(")")[0]  # crude parsing
        item = self.db.items[item_id]


        success, msg = self.db.remove_item(item_id, cascade=False)

        if not success:
            reply = QMessageBox.question(
                self,
                "Item in recipes",
                f"{msg}\nDo you want to remove the item and all its recipes?",
                QMessageBox.Yes | QMessageBox.No
            )
        
            if reply == QMessageBox.Yes:
                success, msg = self.db.remove_item(item_id, cascade=True)
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
            list_item = QListWidgetItem(f"{i.name} ({i.id})")
            list_item.setData(Qt.UserRole, i.id)
            self.items_list.addItem(list_item)
    
    def refresh_recipes_list(self):
        self.recipes_list.clear()
        for r in self.db.recipes:
            list_item = QListWidgetItem(str(r))
            list_item.setData(Qt.UserRole, r)
            self.recipes_list.addItem(list_item)

app = QApplication(sys.argv)

window = MainWindow()
window.show()

sys.exit(app.exec())