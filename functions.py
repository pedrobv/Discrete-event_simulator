import simpy
import numpy as np

class Cycle_time():
    def __init__(self, Env, Process, Model, Equipment):
        self.Env = Env
        self.Process = Process
        self.Model = Model
        self.Equipment = Equipment
        self.Store_creator()
        
    def Create_process(self, layer):
        R = np.random.normal(1, 0.1)
        
        P_time = self.Previous()
        S_time = self.Subsequent()
        Travel = self.T_factor()
        Speed = self.S_factor()
        
        if self.Process.Increase:
            self.Process.Qty += self.Model.Pcs_mod
            M_time = (Travel / Speed) * self.Model.Pcs_mod + (self.Equipment.Specific_h_in + self.Equipment.Specific_h_out) * R # Uniform distribution
        else:
            self.Process.Qty += 1
            M_time = (Travel / Speed) + (self.Equipment.Specific_h_in + self.Equipment.Specific_h_out) * R # Uniform distribution
        
        T_time = P_time + M_time + S_time
        
        yield self.Env.timeout(T_time) # Stop time while is processing
        self.Process.Main_time += M_time # Accumulates process times
        self.Process.Transport_time += self.Transport()
        self.Process.Handling_time += self.Handling()
        print(" \\o/ %s has passed %s process in %.2f minutes" % (layer, self.Process.Name, T_time))

    def Previous(self):
        R = np.random.normal(1, 0.1)
        return (self.Equipment.Distance_p / 64.00 + self.Model.Hand_i) * R

    def Subsequent(self):
        R = np.random.normal(1, 0.1)
        return (self.Equipment.Distance_n / 64.00 + self.Model.Hand_o) * R

    def Transport(self):
        R = np.random.normal(1, 0.1)
        return (self.Equipment.Distance_p + self.Equipment.Distance_n) * R / 64.00

    def Handling(self):
        R = np.random.normal(1, 0.1)
        return (self.Model.Hand_i + self.Model.Hand_o) * R

    def T_factor(self):
        if self.Process.Kind == "Perimeter":
            return self.Model.Perimeter
        elif self.Process.Kind == "Kiss-cut":
            return self.Model.Kc_long
        elif self.Process.Kind == "Unit":
            return 1
        elif self.Process.Kind == "Wire":
            return self.Model.Wire_long

    def S_factor(self):
        return (self.Equipment.Max_s - self.Equipment.Min_s)*np.random.normal(1, 0.1) + self.Equipment.Min_s # uniform distribution

    def Store_creator(self):
        self.Store = simpy.Store(self.Env)

    def Put(self, Item):
        self.Store.put(Item)

    def Get(self):
        return self.Store.get()            

class Schedule():

    def __init__(self, Plant, Shifts, I_stock):
        self.Env = simpy.Environment()
        self.Plant = Plant
        self.Sim_time = Shifts * 7.5 * 60
        self.I_stock = I_stock
        self.Lines_list = []
        self.Resource = []
        self.Store_creator()
        self.Line_generator()
        self.Resource_creator()
    
    def Resource_creator(self):
        for Equipment in self.Plant.Equipments:
            self.Resource.append([Equipment.Name, simpy.Resource(self.Env, Equipment.Operators)])

    def Store_creator(self):
        self.I_store = simpy.Container(self.Env, init = self.I_stock) # initial store
        self.F_store = simpy.Store(self.Env) # final store

    def Put(self, Item):
        self.F_store.put(Item)

    def Get(self, Area):
        return self.I_store.get(Area)

    def Line_generator(self):
        P_list = []
        Line = []
        for Model in self.Plant.Models:
            for Process in self.Plant.Processes:
                P_list.append(Cycle_time(self.Env, Process, Model, Process.Equipment))
            Line.append(P_list)
            Line.append(Model.Name)
            self.Lines_list.append(Line)

    def Get_resource(self, Resource_list, Name):
        for Resource in Resource_list:
            if Resource[0] == Name:
                return Resource[1]

    def Execute_line(self, Cycle_time, N_cycle_time, Mod):
        Resource = self.Get_resource(self.Resource, Cycle_time.Equipment.Name)
        with Resource.request() as Request:
            yield Request
            Input = yield Cycle_time.Get()
            Get_into = self.Env.now
            Wait = Get_into - Input[1]
            Cycle_time.Process.Wait_time += Wait
            print("---> %s get into the %s process at %.2f minutes, having waited %.2f minutes" % (Input[0], Cycle_time.Process.Name, Get_into, Wait))
            process = self.Env.process(Cycle_time.Create_process(Input[0]))
            yield process
            Leaves = self.Env.now
            print("<--- %s leaves the %s process at %.2f minutes" % (Input[0], Cycle_time.Process.Name, Leaves))
            self.Plant.Finish_time = Leaves
            
            if Cycle_time.Process.Increase:
                for j in range(Cycle_time.Model.Pcs_mod):
                    k = Cycle_time.Model.Pcs_mod * (Mod - 1) + j + 1
                    if not N_cycle_time:
                        self.Put("Layer %s %s" % (Cycle_time.Model.Name, k))
                        print("-<>- Layer %s %s was storaged at %s Warehouse at %.2f minutes" % (Cycle_time.Model.Name, k, self.Plant.Name, self.Env.now))
                    else:
                        N_cycle_time.Put(["Layer %s %s" % (Cycle_time.Model.Name, k), self.Env.now])
                        print("-<>- Layer %s %s was storaged at %s storage at %.2f minutes" % (Cycle_time.Model.Name, k, N_cycle_time.Process.Name, self.Env.now))
            else:
                if not N_cycle_time:
                    self.Put("Layer %s %s" % (Cycle_time.Model.Name, Mod))
                    print("-<>- Layer %s %s was storaged at %s Warehouse at %.2f minutes" % (Cycle_time.Model.Name, Mod, self.Plant.Name, self.Env.now))
                else:
                    N_cycle_time.Put(["Layer %s %s" % (Cycle_time.Model.Name, Mod), self.Env.now])
                    print("-<>- Layer %s %s was storaged at %s storage at %.2f minutes" % (Cycle_time.Model.Name, Mod, N_cycle_time.Process.Name, self.Env.now))

    def Run_production(self):
        for Line in self.Lines_list:
            Mod = 0
            while True:
                Mod += 1
                self.Get(Line[0][0].Model.Area) # Removing material from SPD or PDLC rolls
                yield self.Env.timeout(0.001)
                Line[0][0].Put(["%s base material %s" % (Line[0][0].Model.Name, Mod), self.Env.now])
                for k, Cycle_time in enumerate(Line[0]):
                    if not k == len(Line[0]) - 1:
                        self.Env.process(self.Execute_line(Cycle_time, Line[0][k + 1], Mod))
                    else:
                        self.Env.process(self.Execute_line(Cycle_time, None, Mod))

    def Simulate(self):
        self.Env.process(self.Run_production())
        self.Env.run(until = self.Sim_time)

    def Show_results(self):
        Total_pcs = 0
        print("Obtained results:\n")
        for Line in self.Lines_list:
            for Process in Line[0]:
                print("The process rate of %s is %.2f s/pc" % (Process.Process.Name, (Process.Process.Main_time 
                + Process.Process.Transport_time + Process.Process.Handling_time) * 60.0 / Process.Process.Qty))
                print("Transport time in %s process is %.2f s" % (Process.Process.Name, Process.Process.Transport_time * 60.0))
                print("Productive time in %s process is %.2f s" % (Process.Process.Name, Process.Process.Main_time * 60.0))
                print("Handling time in %s process is %.2f s" % (Process.Process.Name, Process.Process.Handling_time * 60.0))
                print("%.2f pieces have been produced in %s process" % (Process.Process.Qty, Process.Process.Name))
                print("Average waiting time: %.2f s" % (Process.Process.Wait_time * 60.0 / Process.Process.Qty))
                print("Stored pieces in %s process: %.2f\n" % (Process.Process.Name, len(Process.Store.items)))
        print("Total worked time: %.2f" % (self.Plant.Finish_time * 60.0))
        print("Total pieces: %.2f" % len(self.F_store.items))
        print("Global average flow rate: %.2f s/pc" % (self.Plant.Finish_time * 60.0 / len(self.F_store.items)))
