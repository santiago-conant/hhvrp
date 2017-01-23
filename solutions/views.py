from django.shortcuts import render

from .models import Solution, Route, RouteSequence
from problems.models import Customer, Problem
from .forms import SAparameters
from .simulated_annealing import *

def route_selection(request):
        routes = Route.objects.all()
        context = {'routes': routes, 'routesCount':Route.objects.count()}
        return render(request, 'solutions/route_selection.html', context)

def route_display(request, route_id):
	customers = RouteSequence.objects.filter(route__id = route_id)
	context = { 'route_id': route_id, 'customers': customers}
	return render(request, 'solutions/route_display.html', context)

def problem_selection(request):
        problems = Problem.objects.all()
        context = {'problems': problems, 'problemsCount':Problem.objects.count()}
        return render(request, 'solutions/problem_selection.html', context)

def solution_selection(request):
        solutions = Solution.objects.all()
        context = {'solutions': solutions}
        return render(request, 'solutions/solution_selection.html', context)

def solution_display(request, solution_id):
        solution = Solution.objects.get(id = solution_id)
        routes = Route.objects.filter(solution=solution)
        rs = []
        for r in routes:
                custs = RouteSequence.objects.filter(route__id = r.id)
                rs.append(custs)
        context = {'routes': rs}
        return render(request, 'solutions/solution_display.html', context)

def create_route(request, problem_id):
        problem = Problem.objects.get(id = problem_id)
        custs = problem.customers.all()
        solution = Solution(problem=problem)
        solution.save()
        route = Route(solution=solution)
        route.save()
        for pos, cust in enumerate(custs):
                customer = RouteSequence(route=route, customer=cust, position=pos)
                customer.save()
        customers = RouteSequence.objects.filter(route__id = route.id)
        context = { 'route_id': route.id, 'customers': customers}
        return render(request, 'solutions/route_display.html', context)
        
def solve_problem(request):
        # if this is a POST request we need to process the form data
        if request.method == 'POST':
                # create a form instance and populate it with data from the request:
                form = SAparameters(request.POST)
                # check whether it's valid:
                if form.is_valid():
                        problem = form.cleaned_data['problem']
                        max_time = form.cleaned_data['max_time']
                        max_temp = form.cleaned_data['max_temp']
                        min_temp = form.cleaned_data['min_temp']
                        eq_iter = form.cleaned_data['eq_iter']
                        temp_change = form.cleaned_data['temp_change']
                        username = form.cleaned_data['username']
                        best,custs = simulated_annealing(problem.id, max_time,
                                                         max_temp, min_temp,
                                                         eq_iter, temp_change)
                        # saving the solution in the database
                        solution = Solution(problem = problem,
                                            username = username,
                                            max_time = max_time,
                                            max_temp = max_temp,
                                            min_temp = min_temp,
                                            eq_iter = eq_iter,
                                            temp_change = temp_change,
                                            cost = best.cost())
                        solution.save()
##                        for r in best.routes:
##                                route = Route(solution=solution)
##                                route.save()
##                                for p,c in enumerate(r.customers):
##                                        cid = custs[c].id
##                                        cust = Customer.objects.get(id=cid)
##                                        customer = RouteSequence(route=route,
##                                                                 customer=cust,
##                                                                 position=p)
##                                        customer.save()
                                        
                        # displaying the solution
                        colors = ['#FF0000', '#00FF00', '#0000FF', '#FFFF00',
                                  '#00FFFF', '#FF00FF', '#FFFFFF', '#000000']
                        croutes = []
                        for nr,r in enumerate(best.routes):
                                croute = []
                                for c in r.customers:
                                        croute.append({'name': custs[c].name,
                                                       'latitude': custs[c].latitude,
                                                       'longitude': custs[c].longitude})
                                croutes.append({'color': colors[nr % 8], 'customers': croute})
                        # redirect to a new URL:
                        context = {'user': username,
                                   'cost': '{:,.3f}'.format(best.cost()),
                                   'solution': croutes}
                        return render(request, 'solutions/draw_solution.html', context)

        # if a GET (or any other method) we'll create a blank form
        else:
                form = SAparameters()
   
        return render(request, 'solutions/solve_problem.html', {'form': form})

def list_results(request):
        solutions = Solution.objects.order_by('cost')
        sols = []
        for solution in solutions:
                sols.append({'solution_id': solution.id,
                             'user': solution.username,
                             'problem': solution.problem,
                             'created': solution.created,
                             'cost': '{:,.3f}'.format(solution.cost)})
        context = {'solutions': sols}
        return render(request, 'solutions/list_results.html', context)

def solution_description(request, solution_id):
        solution = Solution.objects.get(id = solution_id)
        context = {'solution': solution, 'cost': '{:,.3f}'.format(solution.cost)}
        return render(request, 'solutions/solution_description.html', context)

