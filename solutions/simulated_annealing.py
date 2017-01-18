# Simulated Annealing for VRPTW
# Author: Santiago E. Conant-Pablos, November 22, 2016

from django.shortcuts import render
from .perturbation import *

def create_neighbor(current, customers):
    """modifies the current solution"""
    candidate = copy.deepcopy(current)
    rroute1 = random.randint(0, candidate.nroutes-1)
    rroute2 = random.randint(0, candidate.nroutes-1)
    if rroute1 == rroute2:
        if not intraroute_2opt(candidate.routes[rroute1], customers):
##            print("fail intraroute 2opt")
##        if not random_intraroute_movement(rpos, candidate.routes[rroute1], customers):
            rpos = random.randint(0, candidate.routes[rroute1].ncustomers-1)
            random_interroute_movement(rpos, rroute1, candidate, customers)
    else:
        if not interroute_2opt(candidate.routes[rroute1],
                               candidate.routes[rroute2],
                               customers):
            #print("fail interroute 2opt")
            rpos = random.randint(0, candidate.routes[rroute1].ncustomers-1)
            random_interroute_movement(rpos, rroute1, candidate, customers)
    return candidate

def should_accept(candidate, current, temp):
    """decides if candidate solution should substitute the current solution"""
    ncost = candidate.cost()
    ccost = current.cost()
    if ncost <= ccost:
        return True
    else:
        return math.exp((ccost - ncost) / temp) >= random.random()

def random_solution(problem):
    """creates a random solution for all the customers of the problem"""
    rcusts = list(range(1,problem.ncustomers))
    random.shuffle(rcusts)
    ncust = problem.ncustomers-1
    solution = Asolution()
    for c in rcusts:
        random_interroute_insertion(c, solution, problem.customers)
    return solution

def render_solution(request, best, custs):
    # displaying the solution
    colors = ['#FF0000', '#00FF00', '#0000FF', '#FFFF00',
              '#00FFFF', '#FF00FF', '#FFFFFF', '#000000']
    croutes = []
    for nr,r in enumerate(best.routes):
        croute = []
        for c in r.customers:
            croute.append({'latitude': custs[c].latitude,
                           'longitude': custs[c].longitude})
        croutes.append({'color': colors[nr % 8], 'customers': croute})
    context = {'solution': croutes, 'customers': custs}
    render(request, 'solutions/draw_solution.html', context)

    
def simulated_annealing(request, prob_id, max_temp, min_temp, eq_iter, temp_change):
    """implements the Simulated Annealing algorithm"""
##    plt.ion()
##    fig = plt.figure()
    problem = VRPTW()
    problem.load_problem(prob_id)
    problem.eliminate_time_windows()
    current = random_solution(problem)
    temp = max_temp
    best = copy.deepcopy(current)
##    best.plot(problem)
##    fig.canvas.draw()
    i = 0
    while temp > min_temp:
        eiter = 0
        while eiter < eq_iter:
            i += 1
            candidate = create_neighbor(current, problem.customers)
            if should_accept(candidate, current, temp): current = candidate
            if candidate.cost() < best.cost():
                best = copy.deepcopy(candidate)
##                best.plot(problem)
##                fig.canvas.draw()
##                render_solution(request, best, problem.customers)
##            print(" > iteration=%d, temp=%g, curr= %g, best=%g" %
##                  (i+1,temp,candidate.cost(), best.cost()))
            eiter += 1
        temp *= temp_change
##    best.plot(problem, True)
##    plt.ioff()
    return best, problem.customers
