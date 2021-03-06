#!/usr/bin/env python3
import scipy.integrate as spi
import numpy as np
import pylab as pl
import time

### --- creates an instance of the city and the behaviour of the disease --- ###
class city_sir_model(object):
    def __init__(self, name, population, density, latitude, longitude, end_time):
        #General info on city
        self.city_name = name
        self.city_pop = population
        self.city_dens = density
        self.city_lat = latitude
        self.city_long = longitude

        #Info on ODE's
        self.num_iterations = 0
        self.beta = .8
        self.gamma = 0.01
        self.time_step = 0.1

        #Initial and final time for simulation
        self.global_time_infected = 0
        self.end_time = end_time
        
        #Initial Conditions
        self.susceptible_init = 1-1e-6
        self.infected_init= 1e-6
        self.recovered_init = 0
        self.initial_conditions = (self.susceptible_init, self.infected_init, self.global_time_infected)

        self.result = []
        self.infected = False

    def infect(self, time):
        self.global_time_infected = time
        self.num_iterations = int(10*(self.end_time - self.global_time_infected))
        self.infected = True
        self.run_eqs()

    def run_eqs(self):
        t_start = self.global_time_infected;
        t_end = self.end_time
        t_inc = self.time_step
        t_range = np.arange(t_start, t_end, t_inc)
        self.result = spi.odeint(self.diff_eqs, self.initial_conditions , t_range)
        # for result in self.result:
        #     print(result)

    def diff_eqs(self,INP,t):
    	equation_list=np.zeros((3))
    	initial_conditions = INP
    	equation_list[0] = - self.beta * initial_conditions[0] * initial_conditions[1]
    	equation_list[1] = self.beta * initial_conditions[0] * initial_conditions[1] - self.gamma * initial_conditions[1]
    	equation_list[2] = self.gamma * initial_conditions[1]
    	return equation_list   # For odeint

    def plot(self):
        pl.subplot(211)
        pl.plot(self.result[:,0], '-g', label='Susceptibles')
        pl.plot(self.result[:,2], '-k', label='Recovereds')
        pl.legend(loc=0)
        pl.title('Program_2_1.py')
        pl.xlabel('Time')
        pl.ylabel('Susceptibles atime_end Recovereds')
        pl.subplot(212)
        pl.plot(self.result[:,1], '-r', label='Infectious')
        pl.xlabel('Time')
        pl.ylabel('Infectious')
        pl.show()

def main():
    sample_model = city_sir_model("ny",1000000,10000,1,1,200)
    print(sample_model.start_time)

    sample_model.run_eqs()
    print(sample_model.get_city_data())
    # print(sample_model.result)

    print(sample_model.result)
        # time.sleep(1)?
    # sample_model.plot()

    # t_start = 0.0; t_end = 70; t_inc = sample_model.time_step
    # t_range = np.arange(t_start, t_end+t_inc, t_inc)
    # print(t_range)



if(__name__ == '__main__'):
    main()
