from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.forms import ModelForm


import datetime
import time

now = datetime.datetime.now()


RACE_CHOICES = [(5, 5), (10, 10), (21, 21), (42, 42), (50, 50), (100, 100)]
RACE_TYPE = [("road", "road"),
             ("trail", "trail"),
             ("triathlon", "triathlon")]
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
        """Return days until race."""
        return (self.date.replace(tzinfo=None) - now.replace(tzinfo=None)).days

    def calculate_trophy(self, profile, trophy):
        # TODO change name to should_earn_trophy to be more clear, also return value
        """Helper function to check if user(profile) earned any trophy for this race.

        Args:
            profile (Profile):
            trophy (Trophy):

        Returns:
            string: String result if already has trophy or new one is earned.
        """

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
        """Check if user(profile) will earn trophy for this race.

        Args:
            profile (Profile):

        Returns:
            string:
        """
        profile_race_lenghts = [r.race_id.length for r in profile.my_finished_races]
        profile_race_types = [r.race_id.type for r in profile.my_finished_races]

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
    club = models.CharField(choices=CLUB_CHOICES, default="BRC", max_length=50, null=True)
    birth_date = models.DateField(auto_now_add=True, null=True)
    started_running = models.DateField(verbose_name="User started to run", auto_now_add=True, null=True)


    def __str__(self):
        return f"{self.first_name} -  {self.club}"

    @property
    def next_race(self):
        """Get next race for this user.

        Returns:
            bool or Race: Next race if exists, False if there is no next race.
        """
        my_races = Race.objects.filter(userraces__profile_id=self, date__gte=now)
        return my_races[0] if my_races else False

    @property
    def past_races(self):
        """Get past user races.

        Returns:
            list[Race]: QuerySet of past user races.
        """
        return Race.objects.filter(userraces__profile_id=self, date__lt=now)

    @property
    def future_races(self):
        """Get future user races.

        Returns:
            list[Race]: QuerySet of future user races.
        """
        return Race.objects.filter(userraces__profile_id=self, date__gte=now)

    @property
    def my_trophies(self):
        """Get trophies user has earned.

        Returns:
            UserTrophy: QuerySet of any trophies user has earned.
        """
        return UserTrophy.objects.filter(profile=self)

    def check_earned_trophy(self, trophy):
        """Check if user has this trophy.

        Returns:
            bool: True if earned, False if not.
            """
        result = UserTrophy.objects.get(trophy=trophy)
        return True if result else False

    @property
    def my_records(self):
        """ {
        "5": Race_1
        "10": Race_1,
        "21": Race_34,
        "42": Race_2,

        "international": None,
        "trail": None (best pace?)
        }
        """
        result = {}
        # for race_type in RACE_TYPES......TODO
        for race_len in RACE_CHOICES:
            pb = self.get_pb_for_race_len(race_len[0])
            result.update({race_len[0]:pb})
        return result

    def get_pb_for_race_len(self, race_len):
        """Return user PB for race length, None if not ran this race type.
        #TODO zameni da se koristi enum a ne ovako
        Args:
            race_len (int): Race length to check for PB.

        Returns:
            UserRace or None: Race where user had his record
        """
        race_to_search = self.my_finished_races.filter(race_id__length=race_len)
        if not race_to_search:
            return None
        best_race = race_to_search[0]
        for race in race_to_search:
            if race.time <= best_race.time:
                best_race = race

        return best_race

    def get_stats(self):
        """Get user stats like sum of km, number of races, favourite race type.

        Returns:
            dict: Stats `km`, `races`, `favourite`race type
        """
        km_ram = 0
        races_finished = len(self.my_finished_races)
        favourite_race_type = "marathon" #TODO real race type using enum

        for race in self.my_finished_races:
            km_ram += race.race_id.length
        """Return sum of km, time on track, koji """
        result = {"km":km_ram, "races":races_finished, "favourite":favourite_race_type}
        # return km_ram, races_finished, favourite_race_type
        return result

    @property
    def my_races(self):
        """Get races that user added to calendar.

        Returns:
            list[Race]: QuerySet containing user races.
        """
        return Race.objects.filter(userraces__profile_id=self)

    @property
    def my_finished_races(self):
        """Get races that user finished.

        Returns:
            list[UserRaces]
        """
        # return Race.objects.filter(userraces__profile_id=self, userraces__finished=True)
        return UserRaces.objects.filter(profile_id=self, finished=True)

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
    time = models.IntegerField(default=0)
    finished = models.BooleanField(default=False)

    def __gt__(self, other):
        if self.race_id.date > other.race_id.date:
            return self

    def __lt__(self, other):
        if self.race_id.date < other.race_id.date:
            return other

    def __str__(self):
        return f"{self.profile_id.first_name} -- {self.race_id.place} {self.race_id.length}"

    # Metoda za racunanje pejsa
    def sec_to_human(self, seconds):
        """Format seconds to hours, minutes, seconds for it to bee human readable.

        Args:
            seconds (int):

        Returns:
            str: H:M:S
        """

        return time.strftime("%H:%M:%S", time.gmtime(seconds))



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

    @property
    def classname(obj):
        return obj.__class__.__name__

class RaceForm(ModelForm):
    class Meta:
        model = Race
        fields = '__all__'


class UserRaceForm(ModelForm):
    class Meta:
        model = UserRaces
        fields = '__all__'
