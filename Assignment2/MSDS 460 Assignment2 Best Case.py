#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 10 17:32:33 2023

@author: johnmhanson
"""
from pulp import LpVariable, LpProblem, lpSum, LpMinimize, value
#create a dictionary of tasks and duration
tasks = {
    'A': {'duration': 5, 'cost': 500},
    'B': {'duration': 10, 'cost': 1000},
    'C': {'duration': 5, 'cost': 500},
    'D1': {'duration': 15, 'cost': 1500},
    'D2': {'duration': 209, 'cost': 20900},
    'D3': {'duration': 188, 'cost': 18800},
    'D4': {'duration': 202, 'cost': 20200},
    'D5': {'duration': 8, 'cost': 800},
    'D6': {'duration': 158, 'cost': 15800},
    'D7': {'duration': 139, 'cost': 13900},
    'D8': {'duration': 4, 'cost': 400},
    'E': {'duration': 10, 'cost': 1000},
    'F': {'duration': 298, 'cost': 29800},
    'G': {'duration': 40, 'cost': 40000},
    'H': {'duration': 42, 'cost': 42000}
}
# create a list of tasks
tasks_list = list(tasks.keys())

# create a dictionary of precedences 
precedences = {'A':[],
               'B': [],
               'C': ['A'],
               'D1':['A'],
               'D2': ['D1'],
               'D3': ['D1'],
               'D4': ['D2','D3'],
               'D5': ['D4'],
               'D6':['D4'],
               'D7': ['D6'],
               'D8': ['D5', 'D7'],
               'E': ['B', 'C'],
               'F': ['D8','E'],
               'G': ['A', 'D8'],
               'H': ['F','G']
               }
                      
# create the LP problem
prob = LpProblem("Critical Path", LpMinimize)

# Create the LP variables
start_times = {task: LpVariable(f"start_{task}", 0, None) for task in tasks_list}
end_times = {task: LpVariable(f"end_{task}", 0, None) for task in
tasks_list}


# Add the constraints
for task in tasks_list:
    prob += end_times[task] == start_times[task] + tasks[task]['duration'], f"{task}_duration"
    for predecessor in precedences[task]:
        prob += start_times[task] >= end_times[predecessor],f"{task}_predecessor_{predecessor}"

# Set the objective function
prob += lpSum([end_times[task] for task in tasks_list])
"minimize_end_times"

# Solve the LP problem
status = prob.solve()

# Print the results
print("Critical Path time:")
for task in tasks_list:
    if value(start_times[task]) == 0:
        print(f"{task} starts at time 0")
    if value(end_times[task]) == max([value(end_times[task]) for task
in tasks_list]):
        print(f"{task} ends at {value(end_times[task])} days in duration")
        # Print solution
print("\nSolution variable values:")
for var in prob.variables():
    if var.name != "_dummy":
        print(var.name, "=", var.varValue)



