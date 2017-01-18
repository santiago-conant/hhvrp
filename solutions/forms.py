from django import forms
from problems.models import Customer, Problem

class SAparameters(forms.Form):
    # initial temperature
    max_temp = forms.FloatField(label='Initial temperature', initial=25.0) 
    # final temperature
    min_temp = forms.FloatField(label='Final temperature', initial=5.0)  
    # iterations at same temperature
    eq_iter = forms.IntegerField(label='Equal iterations', initial=20) 
    # temperature reduction factor
    temp_change = forms.FloatField(label='Temperature change', initial=0.95)  
    # problem to be solved
    problem = forms.ModelChoiceField(label='Problem to solve', queryset=Problem.objects.all())
