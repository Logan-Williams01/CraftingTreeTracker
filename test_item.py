from Item import Item

item = Item("iron", "Iron", 10)
data = item.to_dict()
new_item = Item.from_dict(data)

print(item)
print(repr(item))


assert item.id == new_item.id
assert item.name == new_item.name
assert item.sell_value == new_item.sell_value


print("Item serialization test passed.")
