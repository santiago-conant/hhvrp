from django.conf.urls import url

from . import views

app_name = 'solutions'
urlpatterns = [
    url(r'^$', views.route_selection, name='route_selection'),
    url(r'^(?P<route_id>[0-9]+)/$', views.route_display, name='route_display'),
    url(r'^problem/$', views.problem_selection, name='problem_selection'),
    url(r'^problem/(?P<problem_id>[0-9]+)/$', views.create_route, name='create_route'),
    url(r'^solve-problem/$', views.solve_problem, name='solve_problem'),
    url(r'^solution/$', views.solution_selection, name='solution_selection'),
    url(r'^solution/(?P<solution_id>[0-9]+)/$', views.solution_display,
        name='solution_display'),
    url(r'^results/$', views.list_results, name='list_results'),
    url(r'^results/(?P<solution_id>[0-9]+)/$', views.solution_description,
        name='solution_description'),
]
