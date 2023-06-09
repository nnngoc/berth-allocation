from population import Population
from berth import Berth
from vessel import Vessel
import time 

start = time.time()
N = 14
# size = {1:10, 2:15, 3:6, 4:20, 5:5, 6:15, 7:7, 8:6, 9:11, 10:7, 11: 8, 12:9, 13:10, 14:11}
# arrive_time = {1:10, 2:5, 3:0, 4:2, 5:15, 6:12, 7:8,8:6, 9:11, 10:7,11: 8, 12:9, 13:10, 14:11}
# process_time = {1:10, 2:9, 3:5, 4:10, 5:5, 6:8, 7:10, 8:6, 9:11, 10:7,11: 8, 12:9, 13:10, 14:11}
# weight = {1:1, 2:2, 3:1, 4:3, 5:1, 6:1, 7:3, 8:1, 9:1, 10:1, 11: 1, 12:1, 13:1, 14:1}

arrive_time={1: 29, 2: 25, 3: 32, 4: 7, 5: 16, 6: 13, 7: 13, 8: 22, 9: 13, 10: 17, 11: 7, 12: 25, 13: 12, 14: 15, 15: 24, 16: 3, 17: 39, 18: 18, 19: 33}
weight={1: 1, 2: 2, 3: 1, 4: 3, 5: 3, 6: 1, 7: 1, 8: 3, 9: 2, 10: 2, 11: 1, 12: 3, 13: 1, 14: 3, 15: 3, 16: 1, 17: 3, 18: 3, 19: 2}
size={1: 7, 2: 16, 3: 11, 4: 13, 5: 12, 6: 19, 7: 9, 8: 8, 9: 11, 10: 13, 11: 7, 12: 14, 13: 7, 14: 10, 15: 19, 16: 13, 17: 16, 18: 16, 19: 10}
process_time={1: 12, 2: 16, 3: 17, 4: 6, 5: 5, 6: 10, 7: 7, 8: 10, 9: 11, 10: 19, 11: 7, 12: 7, 13: 7, 14: 10, 15: 7, 16: 14, 17: 17, 18: 16, 19: 15}



break_points = [20, 32]

S = 40
T = 200
num_generations = 40
population_size = 1000
max_population_size = 1e10
max_objective = 2000

if __name__ == "__main__":
    vessels = []
    for i in range(1, N + 1):
        vessel = Vessel(i + 1, size[i], process_time[i], arrive_time[i], weight = weight[i])
        vessels.append(vessel)
        

    p = Population(population_size, S, T, break_points, vessels)
    p.generate_population()
    fit = p.genetic(num_generations, population_size, max_population_size)


    tops = [b.objective for b in p.berths]
    idx = tops.index(min(tops))
    print('Best objective value:', min(tops))
    p.berths[idx].export_berth(is_sub=True)

end = time.time() - start
print(end)
