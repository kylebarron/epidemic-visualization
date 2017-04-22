#!/usr/bin/env python3
import time
import numpy as np
import random
import math

### --- graph data structure to connect cities --- ###
class graph(object):
    def __init__(self):
        self.vertices = []
        self.adj_matrix = []
        self.global_time = 0
        self.city_list = []

    def transmit_infection(self, city1 , city2):
        prob = self.adj_matrix[city1][city2]
        if(random.randint(1,math.ceil(1/prob)) == 1 and city_list[city2].infected == False):
            self.city_list[city].infect()


def main():
    test = graph()
    test.transmit_infection()
