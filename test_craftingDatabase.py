from CraftingDatabase import CraftingDatabase
from Recipe import Recipe
from Item import Item
import json
import os

def test_crafting_database():
    # --- Create items ---
    iron = Item("iron", "Iron", 10)
    ingot = Item("iron_ingot", "Iron Ingot", 20)
    copper = Item("copper", "Copper", 15)

    # --- Create recipes ---
    recipe1 = Recipe({"iron": 4}, {"iron_ingot": 2}, type="CRAFT", time=5)
    recipe2 = Recipe({"copper": 3}, {"copper_ingot": 1}, type="CRAFT", time=3)

    # --- Create database ---
    db = CraftingDatabase(name="TestDB")
    assert db.name == "TestDB"
    assert len(db.items) == 0
    assert len(db.recipes) == 0

    # --- Add items ---
    success, msg = db.add_item(iron)
    assert success
    success, msg = db.add_item(ingot)
    assert success
    success, msg = db.add_item(iron)  # duplicate
    assert not success

    # --- Add recipes ---
    success, msg = db.add_recipe(recipe1)
    assert success

    # Test unknown items in recipe
    recipe_bad = Recipe({"gold": 2}, {"gold_ingot": 1})
    success, msg = db.add_recipe(recipe_bad)
    assert not success

    # --- to_dict and from_dict ---
    data = db.to_dict()
    assert data["name"] == "TestDB"
    assert "iron" in data["items"]
    assert "iron_ingot" in data["items"]
    assert len(data["recipes"]) == 1

    # --- Save to JSON using the class method ---
    filename = "test_db.json"
    db.save(filename)

    # --- Load from JSON using the class method ---
    db2 = CraftingDatabase.load(filename)

    # --- Assertions ---
    assert db2.name == db.name
    assert db2.items.keys() == db.items.keys()
    assert len(db2.recipes) == len(db.recipes)

    # --- Clean up ---
    os.remove(filename)

    print("All CraftingDatabase tests passed!")

if __name__ == "__main__":
    test_crafting_database()