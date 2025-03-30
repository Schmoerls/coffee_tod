class MachineEnv():
    def __init__(self, avail_types, avail_strength, avail_temp, avail_quantity):
        self.avail_types = avail_types
        self.avail_strength = avail_strength
        self.avail_temp = avail_temp
        self.avail_quantity = avail_quantity
        
        self.state_types = None
        self.state_strength = None
        self.state_temp = None
        self.state_quantity = None
        
    def avail_inform(self, key):
        if key == 'types':
            return self.avail_types
        elif key == 'strength':
            return self.avail_strength
        elif key == 'temp':
            return self.avail_temp
        elif key == 'quantity':
            return self.avail_quantity
        else:
            return None
        
    def set_state(self, key, value):
        if key == 'types':
            if value in self.avail_types:
                self.state_types = value
        elif key == 'strength':
            if value >= self.avail_strength[0] and value <= self.avail_strength[1]:
                self.state_strength = value
        elif key == 'temp':
            if value >= self.avail_temp[0] and value <= self.avail_temp[1]:
                self.state_temp = value
        elif key == 'quantity':
            if value >= self.avail_quantity[0] and value <= self.avail_quantity[1]:
                self.state_quantity = value
        else:
            return None
        
    def get_states(self):
        types = "known" if self.state_types is None else "defined"
        strength = "known" if self.state_strength is None else "defined"
        temp = "known" if self.state_temp is None else "defined"
        quantity = "known" if self.state_quantity is None else "defined"
        
        return {"types": types, "strength": strength, "temp": temp, "quantity": quantity}
    
    def reset(self):
        self.state_types = None
        self.state_strength = None
        self.state_temp = None
        self.state_quantity = None