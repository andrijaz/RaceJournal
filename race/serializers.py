from rest_framework import serializers
from race.models import *


class RaceSerializer(serializers.HyperlinkedModelSerializer):
    # mora da ima create i update metode, ili rucno ili iz nasledjene klase

    class Meta:
        model = Race
        fields = '__all__'


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class TrophySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Trophy
        fields = '__all__'
        depth = 1


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserRacesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserRaces
        fields = '__all__'


class UserTrophySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserTrophy
        fields = '__all__'
