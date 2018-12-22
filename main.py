import copy
import numpy as np
from Greed import greedy
from SA import SA


def read_file(filename):
  FACTORY_NUM = 0
  CUSTOM_NUM = 0
  cost_of_allocate = []
  f = open('./Instances/' + filename)
  raw_string = f.read()
  f.close()
  line_string = raw_string.split('\n')
  split_line_space = list(map(lambda x: x.split(' '), line_string))
  filter_string = list(map(lambda x:list(filter(lambda a: a!='', x)), split_line_space))
  remove_end_string = list(filter(lambda x: x != [], filter_string))
  end = len(remove_end_string)
  if len(remove_end_string[-1]) == 1:
    end = len(remove_end_string) - 1
  result = list(map(lambda x: list(map(lambda a: float(a), x)), remove_end_string[:end]))
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
  temp = result[next_begin: next_begin + (FACTORY_NUM * CUSTOM_NUM) // 10]
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

def write_file(path, solution, cost, opened):
  f = open(path, 'w')
  f.write(str(cost) + '\n' + str(opened) + '\n' + str(solution))
  f.close()

def check_validity(solution, cost, FACTORY_NUM, CUSTOM_NUM, \
    factory_cost, factory_cap, demand, cost_of_allocate):
  # check
  new_cost = 0
  error = False
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
      error = True
      print(error)
  if new_cost != cost:
    error = True
    print(error)
  return error

if __name__ == "__main__":
  for i in range(1, 72):
    try:
      filename = 'p' + str(i)
      FACTORY_NUM, CUSTOM_NUM, \
      factory_cost, factory_cap, demand, cost_of_allocate = read_file(filename)
      # cost, solution, opened = greedy(FACTORY_NUM, CUSTOM_NUM, \
      # factory_cost, factory_cap, demand, cost_of_allocate)
      sa = SA(FACTORY_NUM, CUSTOM_NUM, \
      factory_cost, factory_cap, demand, cost_of_allocate)
      solution, cost, opened = sa.SA()
      error = check_validity(solution, cost, FACTORY_NUM, CUSTOM_NUM, \
      factory_cost, factory_cap, demand, cost_of_allocate)
      # print(error)
      if not error:
        print('success %d' % i)
        write_file('result/SA/' + filename + '_result.txt', solution, cost, opened)
    except:
      print('error %d' % i)
    
