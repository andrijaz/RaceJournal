import serializers
from rest_framework import generics
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from race.models import *


class RaceList(generics.ListCreateAPIView):
    queryset = Race.objects.all()

    serializer_class = serializers.RaceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [SessionAuthentication, BasicAuthentication]


class RaceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Race.objects.all()
    serializer_class = serializers.RaceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class TrophyDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Trophy.objects.all()
    serializer_class = serializers.TrophySerializer


class TrophyList(generics.ListCreateAPIView):
    queryset = Trophy.objects.all()
    serializer_class = serializers.TrophySerializer


class ProfileList(generics.ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = serializers.ProfileSerializer

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [SessionAuthentication, BasicAuthentication]


class ProfileDetail(generics.RetrieveDestroyAPIView):
    queryset = Profile.objects.all()

    serializer_class = serializers.ProfileSerializer


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class UserDetail(generics.RetrieveDestroyAPIView):
    queryset = User.objects.all()

    serializer_class = serializers.UserSerializer

class UserRacesDetail(generics.RetrieveDestroyAPIView):
    queryset = UserRaces.objects.all()
    serializer_class = serializers.UserRacesSerializer


class UserRacesList(generics.ListCreateAPIView):
    queryset = UserRaces.objects.all()
    serializer_class = serializers.UserRacesSerializer


class UserTrophyList(generics.ListCreateAPIView):
    queryset = UserTrophy.objects.all()
    serializer_class = serializers.UserTrophySerializer

class UserTrophyDetail(generics.RetrieveDestroyAPIView):
    queryset = UserTrophy.objects.all()
    serializer_class = serializers.UserTrophySerializer

@api_view(['GET'])
def api_root(request):
    return Response(
        {
            'profiles': reverse('profile-list', request=request),
            'races': reverse('race-list', request=request),
            'trophy': reverse('trophy-list', request=request),
            'userraces': reverse('userraces-list',request=request),
            'usertrophy': reverse('usertrophy-list', request=request),

        }
    )
