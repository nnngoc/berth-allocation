import numpy as np
import pandas as pd
import random




class Berth():
    def __init__(self, idx, S, T, break_point = [], group = []):
        self.idx = idx
        self.S = S
        self.T = T
        self.berth = np.zeros((S, T + 1), dtype = np.int64)
        self.vessels = []
        self.objective = 1e10
        self.break_point = [0] + break_point + [S]
        self.sub_berths = []
        self.vessel_waiting = []
        self.objective = 1e5
        
        if len(break_point) > 0:
            sbs = []
            for i in range(len(self.break_point) - 1):
                # print('Sub berth {} created!'.format(i + 1))
                sbs.append(SubBerth(i + 1, self.break_point[i + 1] - self.break_point[i], T , self.break_point[i]))
#             self.sub_berths = sorted(self.sub_berths, key = lambda x: x.S, reverse = False)
            self.sub_berths = sbs
    
    def export_berth(self, file = 'temp', is_sub = False):
        if not is_sub:
            pd.DataFrame(self.berth).to_csv(file + '.csv')
        else:
            pd.DataFrame(np.concatenate([sb.berth for sb in self.sub_berths])).to_csv(file + '.csv')
        print('file exported!')
        
    def empty_berth(self):
        self.berth = np.zeros((self.S, self.T + 1), dtype = np.int64)
        self.vessels = []
    
    def add_vessel_waiting(self, vessels):
        ret_v = []
        for v in vessels.copy():
            ret = []
            for sb in self.sub_berths:
                if v.size <= sb.S:
                    ret.append(sb.idx)
            if len(ret) == 0:
                print('NO SUB BERTH ACCEPTED!!!!!!!!!!!!!!!!!!!!!')
            v.sub_berth_set = ret
            ret_v.append(v)
            # print('Vessel {} is waiting'.format(v.idx))
        self.vessel_waiting = ret_v
        return True
    
    def add_new_vessel(self, vessel):
        n, u, v, s, t = vessel.idx, vessel.schedule_time, vessel.arrive_place, vessel.size, vessel.process_time
        
        if np.sum(self.berth[v- 1: v+s -1, u:u+t]) > 0:
            print('Vessel {} can not append to berth at time {} and place {}'.format(vessel.idx, u, v))
            return False
        else:
            self.berth[v- 1: v+s -1, u:u+t] = np.ones((s, t))*n
            self.vessels.append(vessel)
            print('Vessel {} inserted to berth at time {} and place {}'.format(vessel.idx, u , v))
            return True 
    
    def remove_vessel(self, vessel):
        if len(self.vessels) == 0:
            print('No vessel!')
            return False
              
        n = vessel.idx
        self.berth[np.where(self.berth == n)] = 0
        new_vessels = []
        for v in self.vessels:
            if v.idx != n:
                new_vessels.append(v)
        self.vessels = new_vessels
        return True
    
    def count_objective(self):
        count = 0
        for v in self.vessels:
            count += v.weight*(v.schedule_time - v.arrive_time)
        self.objective = count
        return count
    
    def count_objective_subBerth(self):
        count = 0
        for sb in self.sub_berths:
#             print('Count on sub-berth {}'.format(sb.idx))
            count += sb.count_objective()
        self.objective = count
        return count
    
    def insert_best_place(self, v):
        inserted = False
        v.schedule_time = v.arrive_time
        v.arrive_place = 1
        while not inserted:
            inserted = self.add_new_vessel(v)
            if (inserted):
                break
            else:
                if v.arrive_place == self.S - v.size + 1:
                    v.schedule_time = v.schedule_time + 1
                    v.arrive_place = 1
                else:
                    v.arrive_place = v.arrive_place + 1
    def insert_best_place_sb(self):
        vessels = self.vessel_waiting.copy()
        for v in vessels:
            self.sub_berths[v.sub_berth_belong - 1].insert_best_place(v)
        self.count_objective_subBerth()
        return True
    
    def random_insert(self):
        insert_chain = []
        vs = random.sample(self.vessel_waiting, len(self.vessel_waiting))

        for v in vs:
            v.sub_berth_belong = random.choice(v.sub_berth_set)

#         print([v.sub_berth_belong for v in vs])
        self.vessel_waiting = vs
        self.insert_best_place_sb()
        
    def mutate(self, mut_rate = 0.5):
        for v in self.vessel_waiting:
            if random.random() < mut_rate:
                v.sub_berth_belong = random.choice(v.sub_berth_set)
            else:
                continue
        for sb in self.sub_berths:
            sb.empty_berth()
            
        self.insert_best_place_sb()

class SubBerth(Berth):
    def __init__(self, idx, S, T, break_point, group = []):
        super().__init__(idx, S, T)
        self.idx = idx
        self.berth = np.zeros((S, T), dtype = np.int64)
        self.offset = break_point
        self.S = S
        self.T = T
        
        
    def add_new_vessel(self, vessel):
        n, u, v, s, t = vessel.idx, vessel.schedule_time, vessel.arrive_place, vessel.size, vessel.process_time
        
        if np.sum(self.berth[v- 1: v+s -1, u:u+t]) > 0:
#             print('Vessel {} can not append to sub-berth {} at time {} and place {}'\
#                   .format(vessel.idx, self.idx, u, v + self.offset))
            return False
        else:
            self.berth[v- 1: v+s -1, u:u+t] = np.ones((s, t))*n
            self.vessels.append(vessel)
#             print('Vessel {} inserted to sub-berth {} at time {} and place {}'\
#                   .format(vessel.idx, self.idx, u , v +  self.offset))
            return True 
        
    
        