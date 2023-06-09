from pulp import *
from pulp import LpMaximize, LpProblem, LpStatus, LpVariable, lpSum
import random
random.seed(100)
from random import randrange


# Input
vessels = range(1, 15)

ss = 40
a={1: 29, 2: 25, 3: 32, 4: 7, 5: 16, 6: 13, 7: 13, 8: 22, 9: 13, 10: 17, 11: 7, 12: 25, 13: 12, 14: 15, 15: 24, 16: 3, 17: 39, 18: 18, 19: 33}
w={1: 1, 2: 2, 3: 1, 4: 3, 5: 3, 6: 1, 7: 1, 8: 3, 9: 2, 10: 2, 11: 1, 12: 3, 13: 1, 14: 3, 15: 3, 16: 1, 17: 3, 18: 3, 19: 2}
s={1: 7, 2: 16, 3: 11, 4: 13, 5: 12, 6: 19, 7: 9, 8: 8, 9: 11, 10: 13, 11: 7, 12: 14, 13: 7, 14: 10, 15: 19, 16: 13, 17: 16, 18: 16, 19: 10}
p={1: 12, 2: 16, 3: 17, 4: 6, 5: 5, 6: 10, 7: 7, 8: 10, 9: 11, 10: 19, 11: 7, 12: 7, 13: 7, 14: 10, 15: 7, 16: 14, 17: 17, 18: 16, 19: 15}
breaks = {1:20, 2:32}
T = 1000

# s = {}
# a = {}
# p = {}
# w = {}
# for i in range (1,20):
#     s[i] = randrange(5, 20)
#     a[i] = randrange(0, 40)
#     p[i] = randrange(5, 20)
#     w[i] = randrange(1, 4)

# Create the model

# Initialize the decision variables
u = LpVariable.dicts("u",vessels, lowBound=0)
v = LpVariable.dicts("v", vessels, lowBound=0)
c = LpVariable.dicts("c", vessels, lowBound=0)
sigma = LpVariable.dicts("sigma", (vessels, vessels), lowBound=0, upBound=1, cat=LpBinary)
delta = LpVariable.dicts("delta", (vessels, vessels), lowBound=0, upBound=1, cat=LpBinary)
gamma = LpVariable.dicts("gamma", (vessels, breaks), lowBound=0, upBound=1, cat=LpBinary)


#Objective function
model = LpProblem('BAP', LpMinimize)
model += lpSum([w[i]*(c[i] - a[i]) for i in vessels])

# Add the constraints to the model[]
for i in vessels:
    for j in vessels:
        if i != j:
            model += u[j] - u[i] - p[i] - (sigma[i][j] - 1) * T >= 0
            model += v[j] - v[i] - s[i] - (delta[i][j] - 1) * ss >= 0
            model += sigma[i][j] + sigma[j][i] <= 1
            model += delta[i][j] + delta[j][i] <= 1
            model += sigma[i][j] + sigma[j][i] + delta[i][j] + delta[j][i] >= 1

for i in vessels:
    model += p[i] + u[i] == c[i]

for i in vessels:
    model += u[i] >= a[i]
    model += u[i] <= T - p[i]
    model += v[i] >= 0
    model += v[i] <= ss - s[i]

for i in vessels:
    for k in breaks:
        model += breaks[k] * gamma[i][k] <= v[i] + s[i]

for i in vessels:
    for k in breaks:
        model += breaks[k] - v[i] + ss * gamma[i][k] >= 0


for i in vessels:
    for k in breaks:
        # if v[i] >= b[k]:
        model += v[i] - breaks[k]*gamma[i][k] >= 0
        # if v[i] +s[i] < b[k]:
        model += v[i] + s[i] - breaks[k] - gamma[i][k]*ss <= 0
        


status = model.solve()

print(f'objective:{model.objective.value()}')

for var in model.variables():
    print(f'{var.name}: {var.value()}')