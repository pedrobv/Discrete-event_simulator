from classes import *
from functions import *

#Create the Plant
Varioplus = Plant("Varioplus")

# Create all the equipments inside the Plant (Machines and Stations)
# (Name, Min_speed, Max_speed, Operators, Distance_to_previous, Distance_to_next, Specific_handling, Place)
Cnc_laser       = Equipment("CNC Laser Machine",          590.0000,   610.0000, 1, 1.45, 2.0, 0.28, Varioplus)

# Create all the Processes inside the Plant
# (Name, Kind_of_process, Increase_pcs?, Need_mod, Equipment, Place)
Laser_cutting   = Process("Laser cutting",          "Perimeter",    True,   True,   Cnc_laser,      Varioplus)

# Create all the Models inside the Plant
# (Name, Perimeter, Area, Kc_long, Pcs_mod, Mod_time, Hand_i, Hand_o, Place)

Model_1         = Model("Name", 430.40, 11615.59, 320.10, 1.00, 2.15, 1.00, 1.00, Varioplus)

# Scheduling and running

Sch = Schedule(Varioplus, 1, 600000)
Sch.Simulate()
Sch.Show_results()
