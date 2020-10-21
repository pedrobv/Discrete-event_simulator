class Plant():
    
    def __init__(self, Name):
        
        self.Name = Name
        self.Processes = []
        self.Equipments = []
        self.Models = []
        self.Finish_time = 0

        print("%s Plant has been created!" % self.Name)

class Process():
    
    def __init__(self, Name, Kind, Increase, Need_mod, Equipment, Place):
        self.Name = Name
        self.Kind = Kind
        self.Increase = bool(Increase)
        self.Need_mod = bool(Need_mod)
        self.Transport_time = 0
        self.Main_time = 0
        self.Handling_time = 0
        self.Qty = 0
        self.Wait_time = 0
        self.Equipment = Equipment
        Place.Processes.append(self)
        
        print("%s Process has been created!" % self.Name)

class Equipment():
    
    def __init__(self, Name, Min_s, Max_s, Operators, Distance_p, Distance_n, Specific_h_in, Specific_h_out, Place):
        self.Name = Name
        self.Min_s = float(Min_s)
        self.Max_s = float(Max_s)
        self.Operators = int(Operators)
        self.Distance_p = float(Distance_p) # distance from the previous process
        self.Distance_n = float(Distance_n) # distance to the next process
        self.Specific_h_in = float(Specific_h_in) # specific time to get the material inside the machine
        self.Specific_h_out = float(Specific_h_out) # specific time to get the material out of the machine
        Place.Equipments.append(self)
        
        print("Equipment %s has been created!" % self.Name)

class Model():

    def __init__(self, Name, Perimeter, Area, Kc_long, Wire_long, Pcs_mod, Hand_i, Hand_o, Place):
        self.Name = Name
        self.Perimeter = float(Perimeter)
        self.Area = float(Area)
        self.Kc_long = float(Kc_long)
        self.Wire_long = float(Wire_long)
        self.Pcs_mod = int(Pcs_mod)
        self.Hand_i = float(Hand_i)
        self.Hand_o = float(Hand_o)
        Place.Models.append(self)

        print("Model %s has been created!" % self.Name)
