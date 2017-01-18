import math
import matplotlib.pyplot as plt
from geopy.distance import vincenty
from problems.models import Problem

class Acustomer:
    """Customer data in Solomon's VRPTW problems"""
    def __init__(self, i, id, n, x, y, q, e, l, d):
        """Constructs a new customer object"""
        self.customer = i           # customer number
        self.id = id                # customer id
        self.name = n           # customer name
        self.latitude = x           # Y positional coordinate: latitude
        self.longitude = y          # X positional coordinate: longitude
        self.demand = q             # demanded products
        self.ready_time = e         # start of time window
        self.due_date = l           # end of time window
        self.service_duration = d   # service duration
        
    def __repr__(self):
        """Constructs a string with a customer data"""
        c = {}
        c['customer'] = self.customer
        c['id'] = self.id
        c['name'] = self.name
        c['latitude'] = self.latitude
        c['longitude'] = self.longitude
        c['demand'] = self.demand
        c['ready_time'] = self.ready_time
        c['due_date'] = self.due_date
        c['service_duration'] = self.service_duration
        return str(c)

    def distance(self, other):
        """computes the Euclidian distance to other customer"""
        spoint = (self.latitude, self.longitude)
        opoint = (other.latitude, other.longitude)
        return vincenty(spoint, opoint).kilometers

    def time(self, other):
        """computes the time to reach other customer"""
        return self.distance(other)

    def cost(self, other):
        """computes the cost to reach other customer"""
        return self.distance(other)

    def onwindow(self, arrive):
        """determines if arrive time is inside the time window"""
        return arrive >= self.ready_time and arrive <= self.due_date

    def early(self, arrive):
        """determines if arrive time occurs after the time window"""
        return arrive < self.ready_time

    def late(self, arrive):
        """determines if arrive time occurs before the time window"""
        return arrive > self.due_date

    def begin_service(self, arrive):
        """determine the beginning service time for a customer from
           the vehicle arriving time"""
        if self.early(arrive): return self.ready_time
        else: return arrive

    def end_service(self, arrive):
        """determines the ending service time for a customer from
           the vehicle arriving time"""
        return self.begin_service(arrive) + self.service_duration

class VRPTW:
    """Vehicle Routing Problem with Time Windows"""
    def __init__(self):
        """constructs a new empty VRPTW"""
        self.fname = ""         # name of the problem (usually the filename)
        self.nvehicles = 0      # number of available vehicles
        self.capacity = 0       # uniform capacity of vehicles
        self.ncustomers = 0     # number of customers
        self.customers = []     # customers' data
        
    def __repr__(self):
        """Constructs a string with the problem data"""
        p = {}
        p['fname'] = self.fname
        p['nvehicles'] = self.nvehicles
        p['capacity'] = self.capacity
        p['ncustomers'] = self.ncustomers
        p['customers'] = self.customers
        return str(p)
        
    def load_problem(self, problem_id):
        """load a Solomon's VRPTW problem"""
        problem = Problem.objects.get(id = problem_id)
        self.fname = problem.name
##        print('problem = ',self.fname)
        self.nvehicles = problem.nvehicles
##        print('# vehicles = ', self.nvehicles)
        self.capacity = problem.capacity
##        print('capacity of vehicles = ', self.capacity)
        custs = problem.customers.all()
        self.customers = []
        depot = problem.depot
        i = 0
        customer = Acustomer(i, depot.id, depot.name, depot.position.latitude,
                             depot.position.longitude, depot.demand,
                             depot.ready_time, depot.due_date, depot.service_duration)
        self.customers.append(customer)
##        print('Depot',i,':',customer)
        for cust in custs:
            if cust.id != depot.id:
                i += 1
                customer = Acustomer(i, cust.id, cust.name, cust.position.latitude,
                                     cust.position.longitude, cust.demand,
                                     cust.ready_time, cust.due_date, cust.service_duration)
                self.customers.append(customer)
##                print('Customer',i,':',customer)
        self.ncustomers = len(self.customers)       
##        print('# clients = ', self.ncustomers-1)

    def eliminate_time_windows(self):
        """modifies the time windows of all customers to the same size of depot"""
        rt = self.customers[0].ready_time
        #dd = self.customers[0].due_date
        dd = 2000.0
        for i in range(1,self.ncustomers):
            self.customers[i].ready_time = rt
            self.customers[i].due_date = dd

class Aroute:
    """Route data for VRP"""
    def __init__(self):
        """constructs a new route without customers"""
        self.length = 0.0        # distance covered by the vehicle
        self.time = 0.0          # total time including time windows and service
        self.cost = 0.0          # cost for the route
        self.demand = 0.0        # acummulated demand of customers
        self.ncustomers = 0      # number of customers
        self.customers = [0,0]   # service sequence of customers
        self.program = [0.0,0.0] # begin service times for each customer
        
    def __repr__(self):
        r = {}
        r['length'] = self.length    
        r['time'] = self.time        
        r['cost'] = self.cost        
        r['demand'] = self.demand    
        r['ncustomers'] = self.ncustomers 
        r['customers'] = self.customers   
        r['program'] = self.program   
        return str(r)

    def empty(self):
        return self.ncustomers == 0

    def insert(self, position, sequence, customers):
        """insert a customer in a position without counting the depot"""
        if position < 0 or position > self.ncustomers:
            raise NameError("wrong insert position in a route")
        else:
            self.customers = self.customers[:position+1] + sequence \
                             + self.customers[position+1:]
            self.program = self.program[:position+1] + [0.0 for _ in sequence] \
                           + self.program[position+1:]
            self.ncustomers += len(sequence)
            self.update(customers)

    def remove(self, position, n, customers):
        """removes N customers from a position without counting the depot"""
        if position < 0 or position+1 > self.ncustomers:
            raise NameError("wrong remove position in a route")
        elif position+n > self.ncustomers:
            raise NameError("not enough customers to remove in a route")
        else:
            del(self.customers[position+1:position+1+n])
            del(self.program[position+1:position+1+n])
            self.ncustomers -= n
            self.update(customers)

    def plot(self, customers, text=False, style = 'ro'):
        """draw a plot of a route"""
        if text:
            print('customers:', self.customers)
            print('begin service times:', self.program)
            print('     No. customers =', self.ncustomers)
            print('     Schedule time =', self.time)
            print('     Route length  =', self.length)
        xp = [customers[c].longitude for c in self.customers]
        yp = [customers[c].latitude for c in self.customers]
        plt.plot(xp,yp, xp,yp, style)

    def update(self, customers):
        """updates the begin service times for customers starting in a position.
           Also updates the total time and cost."""
        acust = customers[self.customers[0]]
        self.length = 0.0
        self.demand = acust.demand
        atime = acust.begin_service(0.0)
        self.program = [atime]
        for i in range(1,len(self.customers)):
            ccust = customers[self.customers[i]]
            self.length += acust.distance(ccust)
            self.demand += ccust.demand
            arrive = acust.end_service(atime) + acust.time(ccust)
            self.program.append(ccust.begin_service(arrive))
            acust = ccust
            atime = self.program[i]
        self.time = self.program[-1]
        self.cost = self.time

    def customers_late(self, customers):
        """return a list of customers serviced late"""
        vcustomers = []
        for i,c in enumerate(self.customers):
            if customers[c].late(self.program[i]): vcustomers.append(c)
        return vcustomers

    def violate_windows(self, customers):
        """check if the route have customers serviced late"""
        nc = self.ncustomers+1
        position = 0
        while position < nc:
            customer = customers[self.customers[position]]
            if customer.late(self.program[position]):
                return True
            position += 1
        return False

class Asolution:
    """VRP Solution"""
    def __init__(self):
        """Constructs a new empty VRP solution"""
        self.nroutes = 0
        self.routes = []

    def __repr__(self):
        """Constructs a string with the solution data"""
        s = {}
        s['nroutes'] = self.nroutes
        for i,route in enumerate(self.routes):
            s['route'+str(i)] = route
        return str(s)

    def append(self, route):
        """appends a new route to the solution"""
        self.routes.append(route)
        self.nroutes += 1

    def remove(self, n):
        """removes a route from the solution"""
        del self.routes[n]
        self.nroutes -= 1

    def length(self):
        """computes the total length of a solution"""
        return sum([r.length for r in self.routes])

    def time(self):
        """computes the total time of a solution"""
        return sum([r.time for r in self.routes])

    def cost(self):
        """computes the total cost of a solution"""
        return self.length()

    def plot(self, problem, text=False):
        """display the solution, its statistics and its plot"""
        customers = problem.customers
        plt.cla()
        plt.xlabel('X Coordinates')
        plt.ylabel('Y Coordinates')
        plt.title('VRPTW problem: ' + problem.fname)
        if text:
            print(">> SOLUTION <<")
            print("Number of routes =", self.nroutes)
        times = []
        lengths = []
        for i,r in enumerate(self.routes):
            if text:
                print('>> Route',i+1)
                times.append(r.time)
                lengths.append(r.length)
            r.plot(customers, text)
        if text:
            print('Maximum route time =', max(times))
            print('Solution time =', sum(times))
            print('Maximum route length =', max(lengths))
            print('Solution length =', sum(lengths))

