from classes import *
from functions import *

#Create the Plant
Varioplus = Plant("Varioplus")

# Create all the equipments inside the Plant (Machines and Station)
# (Name, Min_s, Max_s, Operators, Distance_p, Distance_n, Specific_h, Place)
Cnc_laser       = Equipment("CNC Laser Machine",          590.0000,   610.0000, 1, 1.45, 2.0, 0.28, Varioplus)
Wrk_stn_1       = Equipment("Work Station Kiss-cut",        8.4258,     9.0707, 1, 1.30, 1.3, 0.12, Varioplus)
Silver_paste    = Equipment("Silver Paste Machine",        90.0000,   110.0000, 1, 2.00, 2.0, 3.17, Varioplus)
Wrk_stn_2       = Equipment("Work Station FPC - Cu Tape",  15.4914,    16.4914, 1, 1.30, 1.3, 0.46, Varioplus)
Wrk_stn_3       = Equipment("Work Station Sealing",        98.7857,   102.3682, 1, 1.30, 1.3, 0.37, Varioplus)
Wrk_stn_4       = Equipment("Work Station Inspection",      2.7450,     3.0560, 1, 1.30, 1.3, 1.06, Varioplus)
Wrk_stn_5       = Equipment("Packaging Chamber",            2.9667,     3.4300, 1, 1.00, 1.0, 1.00, Varioplus)

# Create all the Processes inside the Plant
# (Name, Kind, Increase, Need_mod, Equipment, Place)
Laser_cutting   = Process("Laser cutting",          "Perimeter",    True,   True,   Cnc_laser,      Varioplus)
Kc_and_cleaning = Process("Kiss-cut + cleaning",    "Kiss-cut",     False,  False,  Wrk_stn_1,      Varioplus)
Silver_paste    = Process("Silver paste + curing",  "Kiss-cut",     False,  False,  Silver_paste,   Varioplus)
Fpc_cu_tape     = Process("FPC + cu tape",          "Kiss-cut",     False,  False,  Wrk_stn_2,      Varioplus)
Sealing         = Process("Sealing",                "Perimeter",    False,  False,  Wrk_stn_3,      Varioplus)
Inspection      = Process("Inspection",             "Unit",         False,  False,  Wrk_stn_4,      Varioplus)
Hand_pack       = Process("Handling + Packaging",   "Unit",         False,  False,  Wrk_stn_5,      Varioplus)

# Create all the Models inside the Plant
# (Name, Perimeter, Area, Kc_long, Pcs_mod, Mod_time, Hand_i, Hand_o, Place)

#Jaguar_X391     = Model("Jaguar x391",                  504.20, 12181.42,   47.20,   1.00,  2.75,   1.04,   0.78, Varioplus)
#Mcl_ws_sv       = Model("McLaren Windshield Sun Visor", 241.80,  1953.25,   45.71,   4.00,  2.75,   1.00,   0.80, Varioplus)
#Mcl_ws_po       = Model("McLaren Windshield Portal",     59.90,   228.39,    6.30,  10.00,  2.75,   1.00,   1.00, Varioplus)
#Mcl_sr          = Model("McLaren Split Roof",           160.80,  1440.64,    9.00,   6.00,  2.75,   1.00,   0.80, Varioplus)
#Mcl_rq          = Model("McLaren Rear Quarter",         186.00,  1539.34,   13.80,   6.00,  2.75,   1.00,   0.80, Varioplus)
#Riv_rf          = Model("Rivian A1T PDLC",              428.60, 11863.50,   52.00,   1.00,  2.75,   1.04,   0.78, Varioplus)
#Fer_rq          = Model("Ferrari Rear Quarter",          76.40,   336.41,    8.20,   8.00,  1.75,   1.00,   1.00, Varioplus)
#Tes_f2          = Model("Tesla Falcon 2",               482.00,  15017.35, 185.70,   1.00,  2.95,   1.00,   1.00, Varioplus)
#Vw_413          = Model("Volkswagen 413",               386.70,   9363.84, 191.80,   1.00,  2.15,   1.00,   1.00, Varioplus)
Vw_316          = Model("Volkswagen 316",               430.40,  11615.59, 320.10,   1.00,  2.15,   1.00,   1.00, Varioplus)

# Scheduling and running

Sch = Schedule(Varioplus, 1, 600000)
Sch.Simulate()
Sch.Show_results()
