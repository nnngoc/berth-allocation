import random
import copy
from berth import Berth

class Population():
    def __init__(self, size = 100, S = 40, T = 200, break_points = [], vessels = []):
        self.size = size
        self.berths = []
        self.S = S
        self.T = T
        self.break_points = break_points
        
        temp_berths = []
        for i in range(self.size):
            print('Creating berth {} ..'.format(i + 1))
            b = Berth(i + 1, S, T, break_points)
            b.add_vessel_waiting(copy.deepcopy(vessels))
            temp_berths.append(b)
            print('-------------------')
        self.berths = temp_berths
        self.objective = 1e6
        
    def count_population_objective(self):
        count = 0
        for b in self.berths:
            count += b.count_objective_subBerth()
        self.objective = count
        return count
    
    def generate_population(self):
        print('Start population!')
        for b in self.berths:
            b.random_insert()
        print('{} inividuals created!'.format(len(self.berths)))
        return True
    
    def mutate_population(self, b, mut_rate = 0.05):
        b_cop = copy.deepcopy(b)
        b_cop.idx = self.size + 1

        b_cop.mutate(mut_rate)
        
        return b_cop
    
    
    def recombine_population(self, bw1, bw2, re_rate = 0.7):
        b1 = copy.deepcopy(bw1)
        b2 = copy.deepcopy(bw2)
        ret = []
        i = 0
        while i < len(bw1):
            i += 1
            if random.random() > re_rate:
                ret.append(b1[0])
                re = [b for b in b2 if b.idx == b1[0].idx][0]
                b2.remove(re)
                b1.remove(b1[0])
            else:
                ret.append(b2[0])
                re = [b for b in b1 if b.idx == b2[0].idx][0]
                b1.remove(re)
                b2.remove(b2[0])
        
        new_inividual = Berth(self.size + 1, self.S, self.T, self.break_points)
        new_inividual.add_vessel_waiting(ret)

        new_inividual.insert_best_place_sb()
        
        return new_inividual
    
    def genetic(self, num_generations = 60, population_size = 40, max_population_size = 5000,\
                 mutation_rate = 0.2, max_objective = 1000):
        fit = [self.count_population_objective()]
        print('Initital Objective', fit[0])

        for g in range(num_generations):
            print('------------------- GENERATION {}------------------'.format(g + 2))
            for i in range(population_size):
                if (i + 1) % 100 == 0:
                    print('-------------------- GENERATION {} - TOTAL POPULATION: {}------------------------'.format(g + 2, i + 1))
                if self.size == max_population_size:
                    return fit
                else:
                    parents1, parents2 = random.choices(self.berths,k=2, \
                                                        weights=[1/x.count_objective_subBerth() \
                                                                 for x in self.berths])
                    parents1 = self.mutate_population(parents1, mutation_rate)
                    parents2 = self.mutate_population(parents2, mutation_rate)
                    child = self.recombine_population(parents1.vessel_waiting, parents2.vessel_waiting)
                    self.berths.append(child)
                    self.size += 1
#             self.berths = self.berths[-population_size:]
            fit.append(self.count_population_objective())
            print('------------------ OBJECTIVE: {} ---------------'.format(fit[-1] - fit[-2]))
            if len(fit) >= 3:
                if (fit[-2] - fit[-3]) - (fit[-1] - fit[-2]) < max_objective:
                    return fit

        return fit

        
        
        
        