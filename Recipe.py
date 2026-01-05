# Recipes stores two dictionaries of of inputs and outputs in the form of item_id: quantity
# They also store a type and a time variable, yet unused
# Recipes do NOT store Item objects or even know about them. 
class Recipe:
    def __init__(self, inputs, outputs, type="CRAFT", time=0):
        
        #validate inputs by dict, then str key, then int quantity, and finally positive quantity
        if not isinstance(inputs, dict):
            raise TypeError("Inputs must be a dictionary of item_id -> quantity")
        for item_id, quantity in inputs.items():
            if not isinstance(item_id, str):
                raise TypeError(f"item_id must be a string, got {type(item_id).__name__}")
            if not isinstance(quantity, int):
                raise TypeError(f"Quantity must for {item_id} must be an int, got {type(quantity).__name__}")
            if quantity <=0:
                raise ValueError(f"Quantity for {item_id} must be positive, got {quantity}")
        
        #validate outputs by dict, then str key, then int quantity, and finally positive quantity
        if not isinstance(outputs, dict):
            raise TypeError("Outputs must be a dictionary of item_id -> quantity")
        for item_id, quantity in outputs.items():
            if not isinstance(item_id, str):
                raise TypeError(f"item_id must be a string, got {type(item_id).__name__}")
            if not isinstance(quantity, int):
                raise TypeError(f"Quantity must for {item_id} must be an int, got {type(quantity).__name__}")
            if quantity <=0:
                raise ValueError(f"Quantity for {item_id} must be positive, got {quantity}")
        
        
        self.inputs = inputs
        self.outputs = outputs
        self.type = type.upper()
        self.time = float(time)
    
    #CRAFT: iron x4 -> iron_ingot x2 (time: 0.0)
    def __str__(self):
        inputs_str = ", ".join(f"{k} x{v}" for k, v, in self.inputs.items())
        outputs_str = ", ".join(f"{k} x{v}" for k, v, in self.outputs.items())

        return f"{self.type}: {inputs_str} -> {outputs_str} (time: {self.time})"
    
    #Recipe(inputs={'iron': 4}, outputs={'iron_ingot': 2}, type='CRAFT', time=0.0)
    def __repr__(self):
        return (f"Recipe(inputs={self.inputs}, outputs={self.outputs}, type='{self.type}', time={self.time})")
    
    #Adds comparison between Recipes using ==
    def __eq__(self, other):
        return isinstance(other, Recipe) and \
            self.inputs == other.inputs and \
            self.outputs == other.outputs and \
            self.type == other.type and \
            self.time == other.time


    def to_dict(self):
        return {
                "inputs": self.inputs.copy(), 
                "outputs": self.outputs.copy(),
                "type": self.type,
                "time": self.time
                }
    
    
    #return true if item is used in recipe
    def consumes(self, item_id) -> bool:
        return item_id in self.inputs

    #return true if recipe creates item
    def produces(self, item_id) -> bool:
        return item_id in self.outputs

    @classmethod
    def from_dict(cls, data):
        return cls(
                data["inputs"],
                data["outputs"],
                type=data.get("type", "CRAFT"),
                time=data.get("time", 0)

        )