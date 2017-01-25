# Very basic Simulated Annealing Hyperheuristic for VRPTW
# Author: Santiago E. Conant-Pablos, November 22, 2016

from django.shortcuts import render
from .simulated_annealing import *

def create_neighbor_hh(current, pIntraInter, p2optRmove, customers):
    """modifies the current solution"""
    candidate = copy.deepcopy(current)
    rroute1 = random.randint(0, candidate.nroutes-1)
    if random.random() < pIntraInter:
        # intraroute heuristic
        if random.random() < p2optRmove:
            intraroute_2opt(candidate.routes[rroute1], customers)
        else:
            rpos = random.randint(0, candidate.routes[rroute1].ncustomers-1)
            random_intraroute_movement(rpos, candidate.routes[rroute1], customers)
    else:
        # interroute heuristic
        if random.random() < p2optRmove:
            if candidate.nroutes > 1:
                routes = list(range(0, candidate.nroutes))
                routes.remove(rroute1)
                rroute2 = random.choice(routes)
                interroute_2opt(candidate.routes[rroute1], candidate.routes[rroute2], customers)
        else:
            rpos = random.randint(0, candidate.routes[rroute1].ncustomers-1)
            random_interroute_movement(rpos, rroute1, candidate, customers)
    return candidate

def sa_hyperheuristic(prob_id, pIntraInter, p2optRmove, max_time, max_temp,
                      min_temp, eq_iter, temp_change):
    """implements the Simulated Annealing algorithm"""
##    plt.ion()
##    fig = plt.figure()
    problem = VRPTW()
    problem.load_problem(prob_id)
    problem.eliminate_time_windows(max_time)
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
            candidate = create_neighbor_hh(current, pIntraInter, p2optRmove,
                                           problem.customers)
            if should_accept(candidate, current, temp): current = candidate
            if candidate.cost() < best.cost():
                best = copy.deepcopy(candidate)
##                best.plot(problem)
##                fig.canvas.draw()
##            print(" > iteration=%d, temp=%g, curr= %g, best=%g" %
##                  (i+1,temp,candidate.cost(), best.cost()))
            eiter += 1
        temp *= temp_change
##    best.plot(problem, True)
##    plt.ioff()
    return best, problem.customers
