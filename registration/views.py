from coatl.registration import forms, models, mail
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# There's a three-part registration process. First you register an account,
# then you register your school, then you register the teams and the students
# on your teams.

def register_account(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(BASE_URL_PATH + "registration/school")
    if request.method == 'POST':
        form = forms.RegisterUserForm(request.POST)
        if form.is_valid():
            d = form.cleaned_data
            # Create and log in the user
            User.objects.create_user(d['username'], d['email'], d['password'])
            user = auth.authenticate(username=d['username'], password=d['password'])
            auth.login(request, user)
            return HttpResponseRedirect(BASE_URL_PATH + "registration/school")
    else:
        form = forms.RegisterUserForm()
    context = {
        'form': form,
    }
    context.update(csrf(request))
    return render_to_response("registration/account.html", context)

@login_required
def register_school(request):
    if request.method == 'POST':
        if request.user.school_set.count() > 0:
            school = request.user.school_set.all()[0]
            form = forms.RegisterSchoolForm(request.POST, instance=school)
        else:
            school = None
            form = forms.RegisterSchoolForm(request.POST)
        if form.is_valid():
            if school:
                school.save()
            else:
                s = models.School(**form.cleaned_data)
                s.save()
                s.coaches.add(request.user)
                s.save()
                mail.send_reg_confirmation(s)
            return HttpResponseRedirect(BASE_URL_PATH + "registration/teams")
    else:
        if request.user.school_set.count() > 0:
            school = request.user.school_set.all()[0]
            form = forms.RegisterSchoolForm(instance=school)
        else:
            form = forms.RegisterSchoolForm()
    context = {
        'form': form,
    }
    context.update(csrf(request))
    return render_to_response("registration/school.html", context)

@login_required
def register_teams(request):
    if request.user.school_set.count() == 0:
        # No schools? Go and make one
        return HttpResponseRedirect(BASE_URL_PATH + 'registration/school')

    school = request.user.school_set.all()[0]

    if request.method == 'POST':
        teams = forms.TeamFormSet(request.POST, instance=school)
        if teams.is_valid():
            teams.save_all(school=school)
            return HttpResponseRedirect(BASE_URL_PATH + "registration/done")
    else:
        if school.team_set.count() > 0:
            teams = forms.TeamFormSet(instance=school)
        else:
            teams = forms.TeamFormSet()
    context = {
        'teams': teams,
    }
    context.update(csrf(request))
    return render_to_response("registration/teams.html", context)

def index(request):
    return render_to_response("registration/index.html", {})

def done(request):
    return render_to_response("registration/done.html", {})
