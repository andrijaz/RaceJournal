from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from django.db.models import Q

from .models import *
from .forms import ProfileForm
from race.helper import human_to_seconds

from itertools import chain


def index(request):
    return render(request, 'race/index.html')


@login_required
def profile(request):
    profile = request.user.profile
    all_races = Race.objects.filter(userraces__profile_id=request.user.profile)

    context = {'all_races': all_races, 'profile': profile}
    return render(request, 'race/profile.html', context)

def edit_profile(request, pk=None):

    from django.http import HttpResponseForbidden

    form = ProfileForm(request.POST or None, instance=profile)

    if request.POST and form.is_valid():
        form.save()
    # redirect do profila ?
    #     return redirect('profile')
    return render(request, 'race/edit_profile.html', {"form": form})

def edit_profile2(request):

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=Profile)
        # edit_user = Profile.objects.get(profile)

        if form.is_valid():
            form.save(commit=False)

    else:
        edit_user = Profile.objects.get(pk=request.user.profile.pk)
        form = ProfileForm(instance=edit_user)

    # return render(request, 'race/edit_profile.html', {"form": form})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            password = form.cleaned_data['password2']
            username = form.cleaned_data['username']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('edit-profile', pk=user.profile.id)
            # return redirect('profile') pa onda poruka da se popuni profil
    else:
        form = UserCreationForm()
        # form = ProfileForm()
    return render(request, 'registration/register.html', {"form": form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user=user)
            return redirect(to='index')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return render(request, 'registration/logout.html')


@login_required
def explorer(request):
    """Search and filter races."""
    races_to_show = Race.objects.all()
    if request.method == 'POST':

        form = dict(request.POST)
        if form.get('race_length'):
            lengths_to_filter = [int(l) for l in form.get("race_length", None)]
            races_to_show = Race.objects.filter(length__in=lengths_to_filter)

        if form.get('race_type'):
            types_to_show = [t for t in form.get("race_type")]
            races_to_show = races_to_show.filter(type__in=types_to_show)

        if form.get('finished_race'):
            races_to_show = races_to_show.filter(userraces__finished=True,
                                                 userraces__profile_id=request.user.profile.id)
        if form.get('my_races'):
            races_to_show = races_to_show.filter(userraces__profile_id=request.user.profile.id)

    context = {'races': races_to_show}

    return render(request, 'race/explorer.html', context)


@login_required
def add_race(request):
    """View for adding new race to website."""
    if request.method == 'POST':
        form = RaceForm(request.POST)
        if form.is_valid():
            form.save()
            # FIXME mozda ce morati sa javaskript strane da se uradi
            # ako se stiklira finished onda da se upale polja za vreme
            if request.POST['finished'] == 'on':
                race_time = human_to_seconds(request.POST["hours"], request.POST["minutes"], request.POST["seconds"])

                ur = UserRaces(race_id=form.instance, profile_id=request.user.profile, finished=True, time=race_time)
                ur.save()
            return redirect('explorer')
    else:
        form = RaceForm()
    return render(request, 'race/add_race.html', {'form': form})


@login_required
def race_detail(request, pk):
    """View for  detailed race info, add to calendar or add as finished."""

    race = Race.objects.get(pk=pk)
    user_race = UserRaces.objects.filter(race_id=race, profile_id=request.user.profile)

    if request.method == 'GET':
        if user_race and user_race[0].finished:
            # User finished race, show his race result
            finished = True
            race_to_show = user_race[0]
            in_calendar = True
        elif user_race:
            # User added to calendar, countdown days to race
            finished = False
            race_to_show = user_race[0]
            in_calendar = True
        else:
            # Not in calendar, show race info
            finished = False
            race_to_show = race
            in_calendar = False

        return render(request, 'race/race_detail.html', {
            "finished": finished,
            "in_calendar": in_calendar,
            'race': race_to_show,
            'profile': request.user.profile
        })
    if request.method == 'POST':
        # u kalendaru i nije trcao -> da izbaci
        # u kalendaru i tcao -> info

        # nije u kalendaru -> da doda u kalendar
        # nije u kalendaru -> da doda kao istrcanu

        if "remove" in request.POST and user_race:
            # Race is in calendar and user wants to remove it
            # Nekad ne radi lepo jer ima 2 objektasa istim race_id i profile_id
            race_to_remove = UserRaces.objects.get(race_id=race, profile_id=request.user.profile)
            race_to_remove.delete()
            return render(request, 'race/race_detail.html', {
                "finished": False,
                "in_calendar": False,
                'race': race,
                'profile': request.user.profile
            })

        elif "finished" in request.POST:
            # Add race as finished in UserRaces

            # Calculate time in seconds
            # move to helper function
            hour = int(request.POST['hours']) if request.POST['hours'] else 0
            minutes = int(request.POST['minutes']) if request.POST['minutes'] else 0
            seconds = int(request.POST['seconds']) if request.POST['seconds'] else 0
            race_time = hour * 3600 + minutes * 60 + seconds
            finished = True if race_time > 0 else False
            ur = UserRaces(race_id=race, profile_id=request.user.profile, time=race_time, finished=finished)
            ur.save()

            return render(request, 'race/race_detail.html', {
                "finished": finished,
                "in_calendar": True,
                'race': ur,
                'profile': request.user.profile
            })
        elif "to run" in request.POST:
            # Add race to calendar
            ur = UserRaces(race_id=race, profile_id=request.user.profile, time=0, finished=False)
            ur.save()
            return render(request, 'race/race_detail.html', {
                "finished": False,
                "in_calendar": True,
                'race': ur,
                'profile': request.user.profile
            })

        return render(request, 'race/race_detail.html', {'race': race, 'profile': request.user.profile})


@login_required
def timeline(request):
    """Timeline for races, trophies, records, semesters in club."""
    timeline_races = request.user.profile.my_finished_races
    timeline_trophies = request.user.profile.my_trophies
    from helper import sort_results
    result_list = list(chain(timeline_races, timeline_trophies))
    result_list = sort_results(request.user.profile)
    return render(request, 'race/timeline.html', {'timeline_objects': result_list})


def search_all(request):
    q = request.GET['q']

    races = Race.objects.filter(Q(name__icontains=q) |
                                Q(type__icontains=q) |
                                Q(place__icontains=q)).distinct()

    people = Profile.objects.filter(Q(first_name__icontains=q) |
                                    Q(last_name__icontains=q)).distinct()

    result_list = list(chain(races, people))
    return render(request, 'race/search.html', {'result': result_list})
