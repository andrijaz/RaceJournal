from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.forms import ModelForm


import datetime

now = datetime.datetime.now()


RACE_CHOICES = [(5, 5), (10, 10), (21, 21), (42, 42), (50, 50), (100, 100)]
RACE_TYPE = [("road", "road"),
             ("trail", "trail"), ]
CLUB_CHOICES = [("BRC", "BRC"), ("TRIBE", "TRIBE"), ("ADIDAS", "ADIDAS")]
TROPHY_CHOICES = [("first halfmarathon", "first halfmarathon"),
                  ("first marathon", "first marathon"),
                  ("first race", "first race"),
                  ("first trail", "first trail")]


class Race(models.Model):
    place = models.CharField(verbose_name="Place of race organization", max_length=100)
    length = models.IntegerField(verbose_name="Length of race in km", choices=RACE_CHOICES, default=21)
    name = models.CharField(verbose_name="Official race name", max_length=100)
    type = models.CharField(verbose_name="Road or Trail", choices=RACE_TYPE, default="road", max_length=100)
    date = models.DateTimeField(verbose_name="Date of race for each year", auto_now_add=True)
    finished = models.BooleanField(verbose_name="True if race is marked as finished", default=False)

    # time = models.IntegerField(verbose_name="Time needed for race, only if finished")
    # occurrence = models.IntegerField(verbose_name="How old is race", auto_created=1)

    # time = models.TimeField()

    class Meta:
        ordering = ['date', 'length']

    def __str__(self):
        return f"{self.place} - {self.type} - {self.length} <<{self.date.date()}>>"

    def __gt__(self, other):
        if self.date > other.date:
            return self

    def __lt__(self, other):
        if self.date < other.date:
            return other

    def days_until(self):
        return (self.date.replace(tzinfo=None) - now.replace(tzinfo=None)).days

    def calculate_trophy(self, profile, trophy):
        """Only single-race trophies atm."""

        if UserTrophy.objects.filter(profile=profile, trophy=trophy):
            return f"User {profile.first_name} already has {trophy} badge"

        else:

            new_user_trophy = UserTrophy(profile=profile,
                                         race_earned=self,
                                         date_earned=self.date,
                                         trophy=trophy
                                         )
            new_user_trophy.save()
            return "New trophy created"

    def trophy_for_race(self, profile):

        profile_race_lenghts = [r.length for r in profile.my_races if r.finished]
        profile_race_types = [r.type for r in profile.my_races if r.finished]

        if self.length == 21 and 21 not in profile_race_lenghts:
            trophy = Trophy.objects.get(name="First halfmarathon")

            return self.calculate_trophy(profile, trophy)
        if self.length == 42 and 42 not in profile_race_lenghts:
            trophy = Trophy.objects.get(name="First marathon")
            return self.calculate_trophy(profile, trophy)

        if self.type == 'trail' and 'trail' not in profile_race_types:
            trophy = Trophy.objects.get(name="First trail")
            return self.calculate_trophy(profile, trophy)

        if len(profile.my_races) == 10:
            trophy = Trophy.objects.get(name="10 races")
            return self.calculate_trophy(profile, trophy)

    @property
    def classname(obj):
        return obj.__class__.__name__

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=30, null=True)
    races = models.CharField(max_length=100, null=True, default='bg')
    club = models.CharField(choices=CLUB_CHOICES, default="BRC", max_length=50, null=True)
    birth_date = models.DateField(auto_now_add=True, null=True)

    # status = trkac, trener, organizator
    # rekordi, PB -> za svaki tip trke
    def __str__(self):
        return f"{self.user.username} - {self.races} - {self.club}"

    @property
    def next_race(self):
        my_races = Race.objects.filter(userraces__profile_id=self, date__gte=now)
        return my_races[0] if my_races else False

    @property
    def past_races(self):
        return Race.objects.filter(userraces__profile_id=self, date__lt=now)

    @property
    def future_races(self):
        return Race.objects.filter(userraces__profile_id=self, date__gte=now)

    @property
    def my_trophies(self):
        return UserTrophy.objects.filter(profile=self)

    def check_earned_trophy(self, trophy):
        result = UserTrophy.objects.get(trophy=trophy)
        return True if result else False

    def get_stats(self):
        """Return sum of km, time on track, koji """
        pass

    @property
    def my_races(self):
        return Race.objects.filter(userraces__profile_id=self)

    @property
    def my_finished_races(self):
        return Race.objects.filter(userraces__profile_id=self, finished=True)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()


class UserRaces(models.Model):
    profile_id = models.ForeignKey(Profile, on_delete=models.CASCADE, default=1)
    race_id = models.ForeignKey(Race, on_delete=models.CASCADE, default=1)

    def __gt__(self, other):
        if self.race_id.date > other.race_id.date:
            return self

    def __lt__(self, other):
        if self.race_id.date < other.race_id.date:
            return other

    def get_original_race(self):
        return Race.objects.get(pk=self.race_id_id)


class Trophy(models.Model):
    name = models.CharField(max_length=30, default='')
    detail = models.CharField(max_length=200)
    # image
    # neki spisak uslova
    # progress? broj trenutnih trka vs broj potrebnih trka

    def __str__(self):
        return f"{self.name} - {self.detail}"

    @property
    def classname(obj):
        return obj.__class__.__name__

class UserTrophy(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    trophy = models.ForeignKey(Trophy, on_delete=models.CASCADE)
    date_earned = models.DateField(auto_now=True)
    race_earned = models.ForeignKey(Race, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.profile} earned {self.trophy} for {self.race_earned} on {self.date_earned}"


class RaceForm(ModelForm):
    class Meta:
        model = Race
        fields = '__all__'


class UserRaceForm(ModelForm):
    class Meta:
        model = UserRaces
        fields = '__all__'
