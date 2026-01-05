#Items hold an id, name, and a sell_value
#The only logic they hold is how to go from Object -> dictionary -> Object


class Item:

    def __init__(self, id, name, sell_value):
        self.id = id
        self.name = name
        self.sell_value = sell_value
    
    #Iron (ID: iron, Sell value: 10)
    def __str__(self):
        return f"{self.name} (ID: {self.id}, Sell value: {self.sell_value})"
    
    #Item(id='iron', name='Iron', sell_value=10)
    def __repr__(self):
        return f"Item(id='{self.id}', name='{self.name}', sell_value={self.sell_value})"
    
    def to_dict(self):
        return {
                "id": self.id, 
                "name": self.name,
                "sell_value": self.sell_value
                }
    

    @classmethod
    def from_dict(cls, data):
        return cls(
                data["id"],
                data["name"],
                data["sell_value"]
        )
    