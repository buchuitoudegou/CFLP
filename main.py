import copy
import numpy as np
from Greed import greedy
from SA import SA

def read_file():
  FACTORY_NUM = 0
  CUSTOM_NUM = 0
  cost_of_allocate = []
  f = open('./Instances/p1')
  raw_string = f.read()
  line_string = raw_string.split('\n')
  split_line_space = list(map(lambda x: x.split(' '), line_string))
  filter_string = list(map(lambda x:list(filter(lambda a: a!='', x)), split_line_space))
  remove_end_string = list(filter(lambda x: x != [], filter_string))
  result = list(map(lambda x: list(map(lambda a: float(a), x)), remove_end_string))
  FACTORY_NUM = int(result[0][0])
  CUSTOM_NUM = int(result[0][1])
  factory_cap = list(map(lambda x: x[0], result[1:FACTORY_NUM+1]))
  factory_cost = list(map(lambda x: x[1], result[1:FACTORY_NUM+1]))
  origin_factory_cap = copy.deepcopy(factory_cap)
  demand = result[FACTORY_NUM+1:FACTORY_NUM+1+CUSTOM_NUM // 10]
  d = []
  for i in range(len(demand)):
    d += demand[i]
  demand = d
  next_begin = FACTORY_NUM+1 + CUSTOM_NUM // 10
  temp = result[next_begin:]
  temp = np.array(temp)
  temp = np.reshape(temp, (1, -1))[0]
  for i in range(CUSTOM_NUM):
    cost_of_allocate.append([])
  idx = 0
  for i in range(FACTORY_NUM):
    for j in range(CUSTOM_NUM):
      cost_of_allocate[j].append(temp[idx])
      idx += 1
  return FACTORY_NUM, CUSTOM_NUM, factory_cost, factory_cap, demand, cost_of_allocate

if __name__ == "__main__":
  FACTORY_NUM, CUSTOM_NUM, \
  factory_cost, factory_cap, demand, cost_of_allocate = read_file()
  sa = SA(FACTORY_NUM, CUSTOM_NUM, \
  factory_cost, factory_cap, demand, cost_of_allocate)
  solution, cost = sa.SA()
  # check
  new_cost = 0
  # path of each customer
  for i in range(CUSTOM_NUM):
    new_cost += cost_of_allocate[i][solution[i]]
  # build factory
  for i in range(FACTORY_NUM):
    if i in solution:
      new_cost += factory_cost[i]
  # check capacity valid
  for i in range(CUSTOM_NUM):
    factory_cap[solution[i]] -= demand[i]
    if factory_cap[solution[i]] < 0:
      print('error')

  print(solution)
  print(cost, new_cost)
