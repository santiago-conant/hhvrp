from django import forms
from problems.models import Customer, Problem

class SAparameters(forms.Form):
    # initial temperature
    username = forms.CharField(label='Your name', initial='Anonymous') 
    # problem to be solved
    problem = forms.ModelChoiceField(label='Problem to solve', queryset=Problem.objects.all())
    # initial temperature
    max_time = forms.FloatField(label='Maximum length of routes', initial=2000.0) 
    # initial temperature
    max_temp = forms.FloatField(label='Initial temperature', initial=25.0) 
    # final temperature
    min_temp = forms.FloatField(label='Final temperature', initial=5.0)  
    # iterations at same temperature
    eq_iter = forms.IntegerField(label='Equal iterations', initial=20) 
    # temperature reduction factor
    temp_change = forms.FloatField(label='Temperature change', initial=0.95)  
