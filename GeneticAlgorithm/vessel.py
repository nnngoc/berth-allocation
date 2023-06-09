import numpy as np
import pandas as pd


class Vessel():
    def __init__(self, idx, size, process_time, arrive_time, schedule_time = 1e10, \
                 arrive_place = 1e10, weight = 1, sub_berth_belong = 0, sub_berth_set = []):
        self.idx = idx
        self.size = size
        self.process_time = process_time
        self.arrive_time = arrive_time
        self.schedule_time = schedule_time
        self.arrive_place = arrive_place
        self.weight = weight
        self.sub_berth_belong = sub_berth_belong
        self.sub_berth_set = sub_berth_set
        print('Object {} created!'.format(idx))
    
    def set_schedule_time(self, schedule_time):
        self.schedule_time = schedule_time
    
    def set_arrive_place(self, arrive_place):
        self.arrive_place = arrive_place
        
    def set_sub_berth_belong(self, sub_berth_belong):
        self.sub_berth_belong = sub_berth_belong
        
    def set_sub_berth_set(self, sub_berth_set):
        self.sub_berth_set.append(sub_berth_set)
            