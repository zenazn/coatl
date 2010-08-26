from coatl.registration import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.contrib.auth.models import User

# There's a three-part registration process. First you register an account,
# then you register your school, then you register the teams and the students
# on your teams.

def register_account(request):
    if request.method == 'POST':
        form = forms.RegisterUserForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect("/")
    else:
        form = forms.RegisterUserForm()
    context = {
        'form': form,
    }
    context.update(csrf(request))
    return render_to_response("registration/account.html", context)
 
def register_school(request):
    if request.method == 'POST':
        form = forms.RegisterSchoolForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect("/")
    else:
        form = forms.RegisterSchoolForm()
    context = {
        'form': form,
    }
    context.update(csrf(request))
    return render_to_response("registration/school.html", context)
 
def register_teams(request):
    if request.method == 'POST':
        teams = forms.TeamFormSet(request.POST)
        if teams.is_valid():
            return HttpResponseRedirect("/")
    else:
        teams = forms.TeamFormSet()
    context = {
        'teams': teams,
    }
    context.update(csrf(request))
    return render_to_response("registration/teams.html", context)
 
