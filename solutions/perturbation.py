from .vrptw import *
import random
import copy

### route modification functions

def intraroute_2opt(route, customers):
    """removes two arcs (i, j) and (u, v) traversed in the same route and
       reconnects the route concerned using arcs (i, u) and (j, v)
       reversing the subsequence from j to u included."""
    if route.ncustomers < 2: return False
    r = copy.deepcopy(route)
    c1 = random.randint(1,r.ncustomers-1)
    c2 = random.randint(c1+2,r.ncustomers+1)
    #print(c1, c2)
    r.customers[c1:c2] = r.customers[c1:c2][::-1]
    #print(r.customers)
    r.update(customers)
    if r.violate_windows(customers):
        return False
    else:
        route.customers[c1:c2] = r.customers[c1:c2]
        route.update(customers)
        return True

def interroute_2opt(route1, route2, customers):
    """moves two arcs (i, j) and (u, v) in two routes are replaced by
      (i, v) and (u, j)"""
    r1 = copy.deepcopy(route1)
    r2 = copy.deepcopy(route2)
    c1 = random.randint(1,r1.ncustomers)
    c2 = random.randint(1,r2.ncustomers)
    r1cs = r1.customers[:]
    r1.customers[c1:] = r2.customers[c2:]
    r1.ncustomers = len(r1.customers) - 2
    #print(r1cs, r1.customers, r1.ncustomers)
    r1.update(customers)
    if r1.violate_windows(customers): return False
    r2.customers[c2:] = r1cs[c1:]
    r2.ncustomers = len(r2.customers) - 2
    r2.update(customers)
    if r2.violate_windows(customers): return False
    route1.customers[:] = r1.customers
    route1.ncustomers = r1.ncustomers
    route1.update(customers)
    route2.customers[:] = r2.customers
    route2.ncustomers = r2.ncustomers
    route2.update(customers)
    print("succeed interroute 2opt")
    return True

def factible_route_insertion(customer, position, route, customers):
    """determines if a customer can be inserted in a position of a route
       without violating the time windows of customers in a route"""
    r = copy.deepcopy(route)
    r.insert(position, [customer], customers)
    return not r.violate_windows(customers)

def factible_route_positions(customer, route, customers):
    """gets the factible positions to insert a customer inside a route"""
    fpositions = []
    for p in range(0,route.ncustomers+1):
        if factible_route_insertion(customer, p, route, customers):
            fpositions.append(p)
    return fpositions

def random_intraroute_insertion(customer, route, customers):
    """adds a customer to legal random position inside a route"""
    fpositions = factible_route_positions(customer, route, customers)
    #print("customer, factibles = ",customer, fpositions)
    if fpositions:
        npos = random.choice(fpositions)
        route.insert(npos, [customer], customers)
        #print("route = ", route)
        return True
    else: return False

def random_intraroute_movement(position, route, customers):
    """modifies a route moving the customer in a position to a different
       legal random position inside the route"""
    customer = route.customers[position+1]
    route.remove(position,1,customers)
    fpositions = factible_route_positions(customer, route, customers)
    #print("customer, position, factibles = ",customer, position, fpositions)
    fpositions.remove(position)
    if fpositions:
        npos = random.choice(fpositions)
        route.insert(npos, [customer], customers)
        print("Intraroute movement!")
        #print("true, route = ", route)
        return True
    else:
        route.insert(position, [customer], customers)
        #print("false, route = ", route)
        return False

def movable_intraroute_customers(route, customers):
    """gets a list with the position of movable clients in a route"""
    mcust = []
    for c in range(route.ncustomers):
        if len(factible_route_positions(route.customers[c+1],
                                        route,customers)) > 1:
            mcust.append(c)
    return mcust

# solution modification functions

def factible_positions_in_routes(customer, solution, customers):
    """gets a list of factible positions for insertion of a customer
       on the routes of a solution. Do not includes routes without
       factible positions"""
    posbyroute = []
    for i,route in enumerate(solution.routes):
        fpos = factible_route_positions(customer, route, customers)
        if fpos != []: posbyroute.append((i,fpos))
    return posbyroute

def random_interroute_insertion(customer, solution, customers):
    """adds a customer to legal random position inside a legal random route.
       creates a new route if no existing route allows the insertion"""
    posbyroute = factible_positions_in_routes(customer, solution, customers)
    #print("posbyroute = ",posbyroute)
    if posbyroute:
        nroute,positions = random.choice(posbyroute)
        ripos = random.choice(positions)
        solution.routes[nroute].insert(ripos, [customer], customers)
    else:
        #print("New route!")
        route = Aroute()
        route.insert(0, [customer], customers)
        solution.append(route)
    #print("solution = ", solution)

def random_interroute_movement(pcust, nroute, solution, customers):
    """modifies a route moving the customer in a position to a
       legal random position inside of a different legal route"""
    oroute = solution.routes[nroute]
    customer = oroute.customers[pcust+1]
    #print(customer, nroute)
    oroute.remove(pcust,1,customers)
    posbyroute = factible_positions_in_routes(customer, solution, customers)
    #print("customer, posbyroute = ",customer, posbyroute)
    posbyroute = [pbr for pbr in posbyroute if pbr[0] != nroute]
    if posbyroute:
        #print("Old route!")
        nr,positions = random.choice(posbyroute)
        ripos = random.choice(positions)
        solution.routes[nr].insert(ripos, [customer], customers)
    else:
        #print("New route!")
        route = Aroute()
        route.insert(0, [customer], customers)
        solution.append(route)
    if oroute.empty():
        #print("Remove empty route!")
        solution.remove(nroute)
    #print("solution = ", solution)

# test code

if __name__ == "__main__":
    #filename = input("Nombre del archivo del problema? ")
    filename = "c101.txt"
    problem = VRPTW()
    problem.load_problem(filename)
    #problem.eliminate_time_windows()
    ncust = problem.ncustomers-1
    customers = problem.customers
    route = Aroute()
    random_intraroute_insertion(random.randint(1,ncust), route, customers)
    print("route = ",route.customers)
    random_intraroute_insertion(random.randint(1,ncust), route, customers)
    print("route = ",route.customers)
    random_intraroute_insertion(random.randint(1,ncust), route, customers)
    print("route = ",route.customers)
    random_intraroute_insertion(random.randint(1,ncust), route, customers) 
    print("route = ",route.customers)
    random_intraroute_insertion(random.randint(1,ncust), route, customers)
    print("route = ",route.customers)
    random_intraroute_insertion(random.randint(1,ncust), route, customers) 
    print("route = ",route.customers)
    random_intraroute_insertion(random.randint(1,ncust), route, customers)
    print("route = ",route.customers)
    random_intraroute_insertion(random.randint(1,ncust), route, customers) 
    print("route = ",route.customers)
    if intraroute_2opt(route,customers):
        print("2opt = ",route.customers)
    if intraroute_2opt(route,customers):
        print("2opt = ",route.customers)
    if intraroute_2opt(route,customers):
        print("2opt = ",route.customers)
    if intraroute_2opt(route,customers):
        print("2opt = ",route.customers)

##    print("movable customers = ", movable_intraroute_customers(route,customers))
##    solution = Solution()
##    random_interroute_insertion(random.randint(1,ncust), solution, customers)
##    random_interroute_insertion(random.randint(1,ncust), solution, customers)
##    random_interroute_insertion(random.randint(1,ncust), solution, customers)
##    random_interroute_insertion(random.randint(1,ncust), solution, customers)
##    random_interroute_insertion(random.randint(1,ncust), solution, customers)
##    random_interroute_insertion(random.randint(1,ncust), solution, customers)
##    random_interroute_insertion(random.randint(1,ncust), solution, customers)
##    solution.plot(problem)
##    plt.show()
##    rroute = random.randint(0, solution.nroutes-1)
##    rpos = random.randint(0, solution.routes[rroute].ncustomers-1)
##    random_interroute_movement(rpos, rroute, solution, customers)
##    solution.plot(problem)
##    plt.show()
##    rroute = random.randint(0, solution.nroutes-1)
##    rpos = random.randint(0, solution.routes[rroute].ncustomers-1)
##    random_interroute_movement(rpos, rroute, solution, customers)
##    solution.plot(problem)
##    plt.show()
##    rroute = random.randint(0, solution.nroutes-1)
##    rpos = random.randint(0, solution.routes[rroute].ncustomers-1)
##    random_interroute_movement(rpos, rroute, solution, customers)
##    solution.plot(problem)
##    plt.show()
##    rroute = random.randint(0, solution.nroutes-1)
##    rpos = random.randint(0, solution.routes[rroute].ncustomers-1)
##    random_interroute_movement(rpos, rroute, solution, customers)
##    solution.plot(problem)
##    plt.show()
   
    
    
    
