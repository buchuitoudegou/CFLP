import copy

def greedy(FACTORY_NUM, CUSTOM_NUM, 
factory_cost, factory_cap, demand, cost_of_allocate):
  origin_factory_cap = copy.deepcopy(factory_cap)
  factory_cap_ = copy.deepcopy(factory_cap)
  cost = sum(factory_cost)
  solution = []
  for idx in range(CUSTOM_NUM):
    d = demand[idx]
    temp = cost_of_allocate[idx]
    d_cost_of_alloc = []
    for i in range(FACTORY_NUM):
      d_cost_of_alloc.append((i, temp[i]))
    d_cost_of_alloc.sort(key=lambda tup: tup[1])
    for tup in d_cost_of_alloc:
      if factory_cap_[tup[0]] >= d:
        solution.append(tup[0])
        factory_cap_[tup[0]] -= d
        cost += tup[1]
        break
  for i in range(FACTORY_NUM):
    if factory_cap_[i] == origin_factory_cap[i]:
      cost -= factory_cost[i]
  return cost, solution