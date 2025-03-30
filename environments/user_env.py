import random

class UserEnv():
    def __init__(self):
        # Available types, strength, temp, and quantity
        self.avail_types = None
        self.avail_strength = None
        self.avail_temp = None
        self.avail_quantity = None
        
        # Selected types, strength, temp, and quantity
        self.state_types = None
        self.state_strength = None
        self.state_temp = None
        self.state_quantity = None
        
        # Range of types, strength, temp, and quantity for unknown availability
        self.range_types = [
            "Espresso",
            "Americano",
            "Latte",
            "Cappuccino",
            "Macchiato",
            "Mocha",
            "Flat White",
            "Cortado",
            "Ristretto",
            "Lungo",
            "Affogato",
            "Red Eye",
            "Black Coffee",
            "Turkish Coffee",
            "Vietnamese Coffee",
            "Irish Coffee",
            "Doppio",
            "Cafe au Lait",
            "Cold Brew",
            "Nitro Coffee"
        ];
        self.range_strength = [1, 20]
        self.range_temp = [1, 20]
        self.range_quantity = [1, 20]
        
        # Request penalty
        self.penalty_types = {"amount": 0, "ref": []}
        self.penalty_strength = {"amount": 20, "ref": ["types"]}
        self.penalty_temp = {"amount": 0, "ref": []}
        self.penalty_quantity = {"amount": 15, "ref": ["types", "strength", "temp"]}
        
    def avail_receive_inform(self, key, value):
        if key == 'types':
            self.avail_types = value
        elif key == 'strength':
            self.avail_strength = value
        elif key == 'temp':
            self.avail_temp = value
        elif key == 'quantity':
            self.avail_quantity = value
        else:
            return None
        
    def request_state(self, key):
        request_penalty = 0
        if key == 'types':
            if self.avail_types is not None:
                random_type = random.choice(self.avail_types)
            else:
                random_type = random.choice(self.range_types)
                
            self.state_types = random_type
        elif key == 'strength':
            if self.avail_types is None:
                request_penalty += self.penalty_strength["amount"]
            if self.state_types is None:
                request_penalty += self.penalty_strength["amount"]
            result = random.choices([True, False], weights=[request_penalty, 100 - request_penalty], k=1)[0]
            #print("Request Strength Penalty: ", request_penalty, " -> Result: ", result, "_Available Types: ", self.avail_types, "_State Types: ", self.state_types)
            if result:
                return None
            
            if self.avail_strength is not None:
                random_strength = random.randint(self.avail_strength[0], self.avail_strength[1])
            else:
                random_strength = random.randint(self.range_strength[0], self.range_strength[1])
            
            self.state_strength = random_strength
        elif key == 'temp':
            if self.avail_temp is not None:
                random_temp = random.randint(self.avail_temp[0], self.avail_temp[1])
            else:
                random_temp = random.randint(self.range_temp[0], self.range_temp[1])
                
            self.state_temp = random_temp
        elif key == 'quantity':
            if self.avail_types is None:
                request_penalty += self.penalty_quantity["amount"]
            if self.state_types is None:
                request_penalty += self.penalty_quantity["amount"]
            if self.avail_temp is None:
                request_penalty += self.penalty_quantity["amount"]
            if self.state_temp is None:
                request_penalty += self.penalty_quantity["amount"]
            if self.avail_strength is None:
                request_penalty += self.penalty_quantity["amount"]
            if self.state_strength is None:
                request_penalty += self.penalty_quantity["amount"]
            result = random.choices([True, False], weights=[request_penalty, 100 - request_penalty], k=1)[0]
            #print("Request Quantity Penalty: ", request_penalty, " -> Result: ", result, " = ", self.avail_types, self.state_types, self.avail_temp, self.state_temp, self.avail_strength, self.state_strength)
            if result:
                return None
            
            if self.avail_quantity is not None:
                random_quant = random.randint(self.avail_quantity[0], self.avail_quantity[1])
            else:
                random_quant = random.randint(self.range_quantity[0], self.range_quantity[1])
                
            self.state_quantity = random_quant
        else:
            return None
        
    def get_states(self):
        types = "defined" if self.state_types is not None else "unkown" if self.avail_types is None else "known"
        strength = "defined" if self.state_strength is not None else "unkown" if self.avail_strength is None else "known"
        temp = "defined" if self.state_temp is not None else "unkown" if self.avail_temp is None else "known"
        quantity = "defined" if self.state_quantity is not None else "unkown" if self.avail_quantity is None else "known"
        
        return {"types": types, "strength": strength, "temp": temp, "quantity": quantity}
    
    def reset(self):
        self.state_types = None
        self.state_strength = None
        self.state_temp = None
        self.state_quantity = None
        
        self.avail_types = None
        self.avail_strength = None
        self.avail_temp = None
        self.avail_quantity = None