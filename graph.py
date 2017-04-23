#!/usr/bin/env python3
import time
import numpy as np
import random
import math
import csv
from sir_model import city_sir_model

### --- graph data structure to connect cities --- ###
class graph(object):
    def __init__(self, max_time):
        self.vertices = []
        self.adj_matrix = []
        self.max_time = max_time
        self.global_index = max_time*10
        self.global_time = np.arange(0,max_time,.1)
        self.city_list = []
        self.nation_data = [[[0]*3]*50]*self.global_index
        self.test = []

    def transmit_infection(self, city1 , city2, time):
        prob = float(self.adj_matrix[city1][city2])
        if(prob != 0):
            if(random.randint(1,math.ceil(1/prob)) == 1 and
                self.vertices[city1].infected == True and
                self.vertices[city2].infected == False):
                self.vertices[city2].infect(time)
                # print("infect at time", time)
                self.test.append(self.vertices[city2].city_name)
                # time.sleep(5)

    def total_transmit(self, time):
        for i in range(len(self.vertices)):
            for j in range(len(self.vertices)):
                if (i!=j):
                    self.transmit_infection(i,j,time)

    def build_nation_data(self):
        for i in range(self.global_index):
            for j in range(len(self.vertices)):
                if(self.vertices[j].global_time_infected == i/10):
                    for k in range(int(self.vertices[j].num_iterations)):
                        self.nation_data[i][j][0] = self.vertices[j].result[k][0]
                        self.nation_data[i][j][1] = self.vertices[j].result[k][1]
                        self.nation_data[i][j][2] = self.vertices[j].result[k][2]

    def populate_inf_times(self):
        for i in self.global_time:
            if (i > 0):
                self.total_transmit(i)


    def load_city_names(self):
        with open('data/index_names.csv', mode='r') as READ_FILE:
            reader = csv.reader(READ_FILE)
            for line in reader:
                self.city_list.append(line[0])


    def load_adj_mat(self):
        with open('data/adjacency_matrix.csv', mode='r') as READ_FILE:
            reader = csv.reader(READ_FILE)
            for line in reader:
                for i in range(len(line)):
                    line[i] = float(math.log(int(line[i])+1))
                    line[i] = line[i]/30000
                self.adj_matrix.append(line)


    def load_vertex_set(self):
        for name in self.city_list:
            temp_city = city_sir_model(name,1,1,1,1,100)
            self.vertices.append(temp_city)
        for city in self.vertices:
            city.run_eqs()

def main():
    test = graph(100)
    test.load_city_names()
    test.load_adj_mat()
    test.load_vertex_set()
    test.vertices[20].infect(0)
    test.populate_inf_times()
    test.build_nation_data()
    print(test.nation_data[20])



if __name__ == '__main__':
    main()
