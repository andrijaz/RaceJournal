from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from rest_framework import generics
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.db.models import Q

from .models import *
from .serializers import RaceSerializer
from itertools import chain


class RaceList(generics.ListCreateAPIView):
    queryset = Race.objects.all()

    serializer_class = RaceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [SessionAuthentication, BasicAuthentication]


class RaceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Race.objects.all()
    serializer_class = RaceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


@api_view(['GET'])
def api_root(request):
    return Response(
        {
            # 'users': reverse('race-list', request=request),
            'races': reverse('race-list', request=request)
        }
    )


def index(request):
    return render(request, 'race/index.html')


@login_required
def profile(request):
    profile = request.user.profile
    all_races = Race.objects.filter(userraces__profile_id=request.user.profile)

    context = {'all_races': all_races, 'profile': profile}
    return render(request, 'race/profile.html', context)


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            # Kreirano na osnovu User modelu znaci da ce napraviti novog usera
            form.save()

            #
            password = form.cleaned_data['password2']
            username = form.cleaned_data['username']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {"form": form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        # form = request.DATA
        if form.is_valid():
            # login user
            user = form.get_user()
            login(request, user=user)
            # homepage
            # ToDo: redirect to the page where the user came from
            return redirect(to='index')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


@login_required
def logout_view(request):
    if request.method == 'POST':
        logout(request)
    return redirect(to='index')
    # return render(request, 'registration/logout.html')

    # logout(request)


@login_required
def explorer(request):
    races_to_show = Race.objects.all()
    if request.method == 'POST':

        form = dict(request.POST)
        # FIXME preraditi koriscenjem Q upita, kao za timeline
        if form.get('race_length'):
            lenghts_to_filter = [int(l) for l in form.get("race_length", None)]
            races_to_show = Race.objects.filter(length__in=lenghts_to_filter)

        if form.get('race_type'):
            types_to_show = [t for t in form.get("race_type")]
            races_to_show = races_to_show.filter(type__in=types_to_show)

        if form.get('finished_race'):
            races_to_show = races_to_show.filter(userraces__finished=True, userraces__profile_id=request.user.profile.id)
        if form.get('my_races'):
            races_to_show = races_to_show.filter(userraces__profile_id=request.user.profile.id)

    context = {'races': races_to_show}

    return render(request, 'race/explorer.html', context)


@login_required
def add_race(request):
    if request.method == 'POST':
        form = RaceForm(request.POST)
        if form.is_valid():
            form.save()
            if request.POST['finished'] == 'on':
                ur = UserRaces(race_id=form.instance, profile_id=request.user.profile, finished=True)
                ur.save()
            return redirect('explorer')
    else:
        form = RaceForm()
    return render(request, 'race/add_race.html', {'form': form})


@login_required
def race_detail(request, pk):
    race = Race.objects.get(pk=pk)
    if request.method == 'POST':
        if race in request.user.profile.my_races:
            race_to_remove = UserRaces.objects.get(race_id=race, profile_id=request.user.profile)

            race_to_remove.delete()

        elif "finished" in request.POST:

            # Calculate time in seconds
            # move to helper function
            hour = int(request.POST['hours']) if request.POST['hours'] else 0
            minutes = int(request.POST['minutes']) if request.POST['minutes'] else 0
            seconds = int(request.POST['seconds']) if request.POST['seconds'] else 0
            race_time = hour * 3600 + minutes * 60 + seconds
            finished = True if race_time > 0 else False
            ur = UserRaces(race_id=race, profile_id=request.user.profile, time=race_time, finished=finished)
            ur.save()
        elif "to run" in request.POST:
            ur = UserRaces(race_id=race, profile_id=request.user.profile, time=0, finished=False)
            ur.save()

    return render(request, 'race/race_detail.html', {'race_info': race, 'profile': request.user.profile})


@login_required
def timeline(request):
    timelline_races = request.user.profile.my_finished_races
    timeline_trophies = request.user.profile.my_trophies

    result_list = list(chain(timelline_races, timeline_trophies))
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
