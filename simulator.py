from classes import *
from functions import *

#Create the Plant
Varioplus = Plant("Varioplus")

# Create all the equipments inside the Plant (Machines and Stations)
# Used units: lenght (m), time (min), area (m2)
# (Name, Min_speed, Max_speed, Operators, Distance_to_previous, Distance_to_next, Specific_handling_in, Specific_handling_out, Plant_to place)
Cnc_laser = Equipment("CNC Laser Machine", 170.00, 190.00, 1, 2.0, 2.0, 1.0, 1.0, Varioplus)

# Create all the Processes inside the Plant
# (Name, Kind_of_process, Increase_pcs?, Need_mod, Equipment, Place)

# Name: the name of the process.
# Kind_of_process: how the process is applied? by kisscut, by lenght, by area, by unit.
# Increase_pcs?: does this process increase pieces? True or False.
# Need_mod: does this procees need modulation? Trued or False.
# Equipment: which equipment are we working on?
# Place: where are we working?

Laser_cutting   = Process("Laser cutting", "Lenght", True, True, Cnc_laser, Varioplus)

# Create all the Models inside the Plant
# (Name, Perimeter, Area, Kc_long, Wire_long, Pcs_mod, Hand_i, Hand_o, Place)

Model_1 = Model("Name", 4.3040, 1.1615, 3.2010, 120.0, 1.00, 1.00, 1.00, Varioplus)

# Scheduling and running

Sch = Schedule(Varioplus, 1, 600000)
Sch.Simulate()
Sch.Show_results()
