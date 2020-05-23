from rest_framework import serializers

from .models import Race, Profile


class RaceSerializer(serializers.HyperlinkedModelSerializer):

    # mora da ima create i update metode, ili rucno ili iz nasledjene klase

    class Meta:
        model = Race
        fields = '__all__'


class ProfileSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Profile
        fields = '__all__'