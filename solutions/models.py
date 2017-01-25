from django.db import models
from problems.models import Customer, Problem

class Solution(models.Model):
    """Solution of VRP problems"""
    # vrp problem solved
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    # date and time of solution's creation
    created = models.DateTimeField(auto_now_add=True, blank=True)
    # Maximum time for a route
    max_time = models.FloatField(default=0.0) 
    # Simulated Annealing initial temperature
    max_temp = models.FloatField(default=0.0) 
    # Simulated Annealing final temperature
    min_temp = models.FloatField(default=0.0)  
    # Simulated Annealing iterations at same temperature
    eq_iter = models.IntegerField(default=0) 
    # Simulated Annealing temperature reduction factor
    temp_change = models.FloatField(default=0.0)  
    # Solution cost
    cost = models.FloatField(default=0.0)  
    
    def __str__(self):
        c = {}
        c['problem'] = self.problem.name
        c['date'] = self.created
        return str(c)

    class Meta:
        ordering = ['created']

class Result(models.Model):
    """Result of HHVRP competition"""
    # vrp problem solved
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    # date and time of solution's creation
    created = models.DateTimeField(auto_now_add=True, blank=True)
    # user name that run the solver
    username = models.CharField(max_length=50)
    # Probability of using the intraroute 2-opt heuristic
    intra2opt = models.FloatField(default=0.0)  
    # Probability of using the interroute 2-optheuristic
    inter2opt = models.FloatField(default=0.0)  
    # Probability of using the intraroute shift heuristic
    intraShift = models.FloatField(default=0.0)  
    # Probability of using the interroute shift heuristic
    interShift = models.FloatField(default=0.0)  
    # Solution cost
    cost = models.FloatField(default=0.0)  
    
    def __str__(self):
        c = {}
        c['problem'] = self.problem.name
        c['date'] = self.created
        c['user'] = self.username
        return str(c)

    class Meta:
        ordering = ['cost']

class Route(models.Model):
    """Route data for VRP problems"""
    # problem that contains the route
    solution = models.ForeignKey(Solution, on_delete=models.CASCADE)
    # distance covered by the vehicle
    length = models.FloatField(default=0.0)
    # total time including time windows and service
    time = models.FloatField(default=0.0)
    # cost for the route
    cost = models.FloatField(default=0.0)
    # acummulated demand of customers
    demand = models.IntegerField(default=0)
    # customers sequence in the route
    customers = models.ManyToManyField(Customer,through='RouteSequence')

    def __str__(self):
        """Constructs a string with a elements of a route sequence"""
        c = {}
        c['problem'] = self.solution.problem.name
        c['date'] = self.solution.created
        c['route'] = self.id
        return str(c)
    
    def __repr__(self):
        """Constructs a string with a elements of a route sequence"""
        c = {}
        c['problem'] = self.solution.problem.name
        c['date'] = self.solution.created
        c['route'] = self.id
        c['length'] = self.length
        c['time'] = self.time
        c['cost'] = self.cost
        c['demand'] = self.demand
        return str(c)

    class Meta:
        ordering = ['solution']

class RouteSequence(models.Model):
    """Sequence of customers in a route"""
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    position = models.IntegerField(default=0)
    
    def __str__(self):
        """Constructs a string with a elements of a route sequence"""
        c = {}
        c['route_id'] = self.route.id
        c['customer'] = self.customer.name
        c['position'] = self.position
        return str(c)

    class Meta:
        ordering = ('route',)
        unique_together = ('route', 'position',)




