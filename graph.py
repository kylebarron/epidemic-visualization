#!/usr/bin/env python3
import time
import numpy as np
import random
import math
import csv
from sir_model import city_sir_model


class data_point(object):
    def __init__(self, s, i, r):
        self.s = s
        self.i = i
        self.r = r

### --- graph data structure to connect cities --- ###
class graph(object):
    def __init__(self, max_t):
        #Graph structure
        self.vertices = []
        self.city_list = []
        self.adj_matrix = []

        #Epidemic Info
        self.max_time = max_t
        self.global_index = self.max_time*10
        self.global_time = np.arange(0,self.max_time,.1)

        self.nation_data = [[0]*50]*self.global_index

    def total_transmit(self, time):
        for i in range(len(self.vertices)):
            for j in range(len(self.vertices)):
                prob = float(self.adj_matrix[i][j])
                if (i!=j and prob != 0 and random.randint(1,math.ceil(1/prob)) == 1 and
                    self.vertices[i].infected == True and
                    self.vertices[j].infected == False):
                    self.vertices[j].infect(time)
                    # print(time)

    def build_nation_data(self):
        for i in range(self.global_index):
            for j in range(len(self.vertices)):
                # print("city#: ", j,"timestamp: ", i, "globalindex: ", self.global_index)
                if(self.vertices[j].global_time_infected <= i/10.0):
                    k = i-self.vertices[j].global_time_infected*10
                    print(k)
                    # temp_dp = data_point(self.vertices[j].result[k][0], self.vertices[j].result[k][1], self.vertices[j].result[k][2])
                    # self.nation_data[i][j] = temp_dp
                    # print("city#: ", j,"timestamp: ", i, "globalindex: ", self.global_index)
                #     # print("--------------------------")
                #     # print("city#: ", j,"timestamp: ", i, "globalindex: ", self.global_index)
        #             for k in range(self.vertices[j].num_iterations):
        #                 temp_dp = data_point(self.vertices[j].result[k][0], self.vertices[j].result[k][1], self.vertices[j].result[k][2])
        #                 self.nation_data[i+k][j] = temp_dp
        #                 print(self.nation_data[i+k][j].s, self.nation_data[i+k][j].i, self.nation_data[i+k][j].r)
        #                 print(i+k, )
        # for i in range(len(self.nation_data[:])):
        #     print(self.nation_data[i][20].s, self.nation_data[i][20].i, self.nation_data[i][20].r )

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
            temp_city = city_sir_model(name,1,1,1,1,self.max_time)
            self.vertices.append(temp_city)

def main():
    sim_time = 10;
    test = graph(sim_time)

    test.load_city_names()
    test.load_adj_mat()
    test.load_vertex_set()

    test.vertices[20].infect(0)
    test.populate_inf_times()
    test.build_nation_data()
    # for i in range(len(test.nation_data[:])):
    #     print(test.nation_data[i][20].s, test.nation_data[i][20].i, test.nation_data[i][20].r )


if __name__ == '__main__':
    main()
