from Item import Item
from Recipe import Recipe

iron = Item("iron", "Iron", 10)
ingot = Item("iron_ingot", "Iron ingot", 20)
copper = Item("copper", "Copper", 10)
recipe = Recipe({"iron": 4}, {"iron_ingot": 2})
data = recipe.to_dict()
new_recipe = Recipe.from_dict(data)

print(recipe)
print(repr(recipe))

assert recipe.consumes("iron") == True
assert recipe.consumes("copper") == False
assert recipe.produces("iron_ingot") == True
assert recipe.produces("copper") == False
assert recipe.inputs == new_recipe.inputs
assert recipe.outputs == new_recipe.outputs
assert recipe.type == new_recipe.type
assert recipe.time == new_recipe.time
assert recipe == new_recipe
print("All tests passed!")