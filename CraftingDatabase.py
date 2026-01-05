from Item import Item
from Recipe import Recipe
import json

# CraftingDatabase stores a name (meant to correlate to a specific game and therefore filename, but not enfored)
# Also stores a Dictionary of item_id: Item(object) and a List of Recipes
# CraftingDatabase is meant to handle all Item and Recipe interaction logic, including enforcing unique Items, Recipes, and calculations involving multiple Items or Recipes 

class CraftingDatabase:
    def __init__(self, items: dict[str, Item]=None, recipes:list[Recipe]=None, name="Unnamed Database"):
        
        self.name = name

        #Defaults to adding empty items and recipes, then overwrites if passed data is valid

        #Ensures passed items is not None, then a dictionary, that each item_id actually matches the Item's id
        self.items = {}
        if items is not None:
            if not isinstance(items, dict):
                raise TypeError(f"items must be a dict, got '{type(items)}'")
            for k, i in items.items():
                if k != i.id:
                    raise ValueError(f"Dictionary key '{k}' does not match Item.id '{i.id}'")
            self.items = items.copy()
        
        #Ensures each dictionary value copied is actually an Item
        for i in self.items.values():
            if not isinstance(i, Item):
                raise TypeError(f"items must contain Item objects, got '{type(i)}'")


        #Ensures passed recipes is not None, then a list
        self.recipes = []
        if recipes is not None:
            if not isinstance(recipes, list):
                raise TypeError(f"recipes must be a list, got '{type(recipes)}'")
            self.recipes = recipes.copy()

        #Ensures each object in recipes is actually a Recipe
        for r in self.recipes:
            if not isinstance(r, Recipe):
                raise TypeError(f"recipes must contain Recipe objects, got '{type(r)}'")
            
        
        
    #Does not allow adding duplicate items
    #Returns a boolean success value and related message
    def add_item(self, item:Item):
        if item.id in self.items:
            return False, "Item already exists"
        self.items[item.id] = item
        return True, "Item successfully added"

    #Does not allow adding duplicate recipes
    #Returns a boolean success value and related message
    def add_recipe(self, recipe:Recipe):
        for r in self.recipes:
            if r == recipe:
                return False, "Recipe already exists"
       
        for item_id in recipe.inputs.keys():
            if item_id not in self.items:
                return False, f"Unknown input item '{item_id}'. Add it before adding the recipe."
       
        for item_id in recipe.outputs.keys():
            if item_id not in self.items:
                return False, f"Unknown output item '{item_id}'. Add it before adding the recipe."

        self.recipes.append(recipe)
        return True, "Recipe successfully added"
    
    #Must convert self.items from a dictionary of item_id: Item(object) to item_id: Item(dictionary) using item.to_dict()
    #Must convert self.recipes from a list of Recipe(object) to a list of Recipe(dictionary) using recipe.to_dict()
    #Finally creates a dictionary of "name": name, "items": dictionary(item_id:Item(dictionary)), "recipes": list(Recipe(dictionary))
    def to_dict(self):
        
        items_dict = {}
        for item_id, item in self.items.items():
            items_dict[item_id] = item.to_dict()
        
        recipes_list = []
        for recipe in self.recipes:
            recipes_list.append(recipe.to_dict())
        
        return { 
            "name": self.name,
            "items": items_dict,
            "recipes": recipes_list
        }

    #Saves the database to a JSON file in self.to_dict() form
    def save(self, filename=None):
        if filename is None:
            filename = f"{self.name}.json"
        with open(filename,"w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=4)


    #Unwraps the nested dictionary and list mess back into objects, using Item's and Recipe's from_dict() methods
    @classmethod
    def from_dict(cls, data):
        
        name = data["name"]

        items = {}
        for item_id, item_data in data["items"].items():
            items[item_id] = Item.from_dict(item_data)
        
        recipes = []
        for recipe_data in data["recipes"]:
            recipes.append(Recipe.from_dict(recipe_data))
        
        return cls(items=items, recipes=recipes, name=name)
    
    #Loads the JSON file's dictionary into a CraftingDatabase object using from_dict()
    @classmethod
    def load(cls, filename):
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        return cls.from_dict(data)
