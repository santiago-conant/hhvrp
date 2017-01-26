from django import forms
from django.forms.widgets import NumberInput
from problems.models import Customer, Problem

class SAparameters(forms.Form):
    # problem to be solved
    problem = forms.ModelChoiceField(label='Problem to solve', queryset=Problem.objects.all())
    # initial temperature
    max_time = forms.FloatField(label='Maximum length of routes(Kms)', min_value=0.0, initial=3000.0) 
    # initial temperature
    max_temp = forms.FloatField(label='Initial temperature', min_value=0.0, initial=25.0) 
    # final temperature
    min_temp = forms.FloatField(label='Final temperature', min_value=0.0, initial=5.0)  
    # iterations at same temperature
    eq_iter = forms.IntegerField(label='Iterations at temperature', min_value=1, initial=20) 
    # temperature reduction factor
    temp_change = forms.FloatField(label='Temperature change factor',
                                   min_value=0.0, max_value=1.0, initial=0.9)  

class CompetitionForm(forms.Form):
    # competitor name
    username = forms.CharField(initial='Anonymous') 
    # probability of using the 2-opt heuristic
    prob_Intra_Inter = forms.IntegerField(widget=NumberInput(attrs={'type':'range', 'step':'1',
                                                                    'min':'0', 'max':'100',
                                                                    'onchange':'updateIntraInter(this.value);'})) 
    # probability of using the 2-opt heuristic
    prob_2opt_Rmove = forms.IntegerField(widget=NumberInput(attrs={'type':'range', 'step':'1',
                                                                    'min':'0', 'max':'100',
                                                                    'onchange':'update2optShift(this.value);'})) 
