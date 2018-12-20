import random
import copy
from scipy import exp

class SA:
  def __init__(self, FACTORY_NUM, CUSTOM_NUM, \
  factory_cost, factory_cap, demand, cost_of_allocate):
    self.FACTORY_NUM = FACTORY_NUM
    self.CUSTOM_NUM = CUSTOM_NUM
    self.factory_cost = copy.deepcopy(factory_cost)
    self.factory_cap = copy.deepcopy(factory_cap)
    self.origin_cap = copy.deepcopy(factory_cap)
    self.demand = copy.deepcopy(demand)
    self.cost_of_allocate = copy.deepcopy(cost_of_allocate)
    self.solution = []
    self.cost = 0.0
  
  def initial_solution(self):
    index = 0
    while len(self.solution) < self.CUSTOM_NUM:
      r = random.random()
      idx = int(r * self.FACTORY_NUM)
      if self.factory_cap[idx] >= self.demand[index]:
        if not idx in self.solution:
          self.cost += self.factory_cost[idx]
        self.solution.append(idx)
        self.factory_cap[idx] -= self.demand[index]
        self.cost += self.cost_of_allocate[index][idx]
        index += 1
    
  def SA(self):
    self.initial_solution()
    T = 1000
    while T > 0.1:
      print(T)
      for i in range(1500):
        new_solution, new_cost = self.get_new_solution()
        if new_cost < self.cost:
          self.solution = copy.deepcopy(new_solution)
          self.cost = new_cost
          self.update_cap()
        else:
          delta = new_cost - self.cost
          probility = exp(-delta / T)
          if probility > random.random():
            self.solution = copy.deepcopy(new_solution)
            self.cost = new_cost
            self.update_cap()
      T *= 0.98
    return self.solution, self.cost
  
  def update_cap(self):
    self.factory_cap = copy.deepcopy(self.origin_cap)
    for i in range(self.CUSTOM_NUM):
      self.factory_cap[self.solution[i]] -= self.demand[i]

  def get_new_solution(self):
    method = int(random.random() * 2)
    solution = copy.deepcopy(self.solution)
    if method == 0:
      c1 = int(random.random() * self.CUSTOM_NUM)
      c2 = int(random.random() * self.CUSTOM_NUM)
      while self.solution[c1] == self.solution[c2] or \
      self.factory_cap[solution[c2]] + self.demand[c2] < self.demand[c1] or \
      self.factory_cap[solution[c1]] + self.demand[c1] < self.demand[c2]:
        c1 = int(random.random() * self.CUSTOM_NUM)
        c2 = int(random.random() * self.CUSTOM_NUM)
      # self.factory_cap[solution[c2]] += self.demand[c2] - self.demand[c1]
      # self.factory_cap[solution[c1]] += self.demand[c1] - self.demand[c2]
      solution[c1], solution[c2] = solution[c2], solution[c1]
    else:
      c1 = int(random.random() * self.CUSTOM_NUM)
      fidx = int(random.random() * self.FACTORY_NUM)
      flag = True
      for i in range(self.FACTORY_NUM):
        if self.factory_cap[i] > self.demand[c1]:
          flag = False
          break
      if flag:
        return solution, self.cost
      while self.factory_cap[fidx] - self.demand[c1] < 0:
        fidx = int(random.random() * self.FACTORY_NUM)
      # self.factory_cap[fidx] -= self.demand[c1]
      solution[c1] = fidx
    new_cost = 0
    for i in range(self.FACTORY_NUM):
      if i in solution:
        new_cost += self.factory_cost[i]
    for i in range(self.CUSTOM_NUM):
      new_cost += self.cost_of_allocate[i][solution[i]]
    return solution, new_cost
  