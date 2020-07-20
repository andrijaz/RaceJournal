from datetime import datetime

from django.db.models import Count
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.forms import ModelForm

from race.helper import RACE_LENGTH, CLUB_CHOICES, RACE_TYPE, GENDER, SHORTS_SIZE, SHIRT_SIZE

from race.helper import get_type_from_length, human_to_seconds, sec_to_human


class Race(models.Model):
    """Represent race with info: when, where, type, length, city."""
    place = models.CharField(verbose_name="Place of race organization", max_length=100)
    length = models.IntegerField(choices=RACE_LENGTH, verbose_name="Length of race in km", default=21)
    name = models.CharField(verbose_name="Official race name", max_length=100)
    type = models.CharField(verbose_name="Type of race, road or trail", choices=RACE_TYPE, max_length=30)
    date = models.DateTimeField(verbose_name="Date of race for each year", auto_now_add=True)

    # occurrence = models.IntegerField(verbose_name="How old is race", auto_created=1)
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
        return (self.date.replace(tzinfo=None) - datetime.now().replace(tzinfo=None)).days

    def should_earn_trophy(self, profile, trophy):
        """Helper function to check if user(profile) earned any trophy for this race.

        Args:
            profile (Profile): Profile to check.
            trophy (Trophy): Trophy object to check.

        Returns:
            bool: True if new trophy created, False if not.
        """

        if UserTrophy.objects.filter(profile=profile, trophy=trophy):
            return False

        else:

            new_user_trophy = UserTrophy(profile=profile,
                                         race_earned=self,
                                         date_earned=self.date,
                                         trophy=trophy
                                         )
            new_user_trophy.save()
            return True

    def trophy_for_race(self, profile):
        """Check if user(profile) will earn trophy for this race.

        Args:
            profile (Profile):

        Returns:
            string:
        """

        profile_race_lengths = [r.race_id.length for r in profile.my_finished_races]
        profile_race_types = [r.race_id.type for r in profile.my_finished_races]

        if self.length == 21 and 21 not in profile_race_lengths:
            trophy = Trophy.objects.get(name="First halfmarathon")

            return self.should_earn_trophy(profile, trophy)
        if self.length == 42 and 42 not in profile_race_lengths:
            trophy = Trophy.objects.get(name="First marathon")
            return self.should_earn_trophy(profile, trophy)

        if self.type == 'trail' and 'trail' not in profile_race_types:
            trophy = Trophy.objects.get(name="First trail")
            return self.should_earn_trophy(profile, trophy)

        if profile.my_races.count() == 10:
            trophy = Trophy.objects.get(name="10 races")
            return self.should_earn_trophy(profile, trophy)

    @property
    def classname(obj):
        return obj.__class__.__name__


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=30, null=True)
    club = models.CharField(verbose_name="Current user club", choices=CLUB_CHOICES, default="BRC", max_length=50,
                            null=True)
    birth_date = models.DateField(null=True)
    started_running = models.DateField(verbose_name="User started to run", null=True)
    gender = models.CharField(choices=GENDER, max_length=10)

    def __str__(self):
        return f"{self.user} - ({self.first_name} {self.last_name} | {self.birth_date}) -  {self.club}({self.started_running})"

    @property
    def next_race(self):
        """Get next race for this user.

        Returns:
            bool or UserRace: Next race if exists, False if there is no next race.
        """
        my_races = UserRaces.objects.filter(profile_id=self, race_id__date__gte=datetime.now())
        return my_races[0] if my_races else False

    @property
    def past_races(self):
        """Get past user races.

        Returns:
            list[UserRace]: QuerySet of past user races.
        """
        return UserRaces.objects.filter(profile_id=self, race_id__date__lte=datetime.now(), finished=True)

    @property
    def future_races(self):
        """Get future user races.

        Returns:
            list[UserRace]: QuerySet of future user races.
        """
        return UserRaces.objects.filter(profile_id=self, race_id__date__gte=datetime.now())

    @property
    def my_races(self):
        """Get races that user added to calendar.

        Returns:
            list[UserRace]: List of all user races.
        """

        return UserRaces.objects.filter(profile_id=self)

    @property
    def my_finished_races(self):
        """Get races that user finished.

        Returns:
            UserRaces: List of finished user races
        """
        return UserRaces.objects.filter(profile_id=self, finished=True)

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
        for race_type in RACE_TYPE:
            pb = self.get_pb_for_race_type(race_type[0])
            result.update({race_type[0]:pb})
        for race_len in RACE_LENGTH:
            pb = self.get_pb_for_race_len(race_len[0])
            result.update({race_len[0]: pb})
        return result

    def get_pb_for_race_type(self, race_type):
        """Return user PB for race type, None if not ran this race type.

        Args:
            race_type (str): Race tyoe to check for PB.

        Returns:
            UserRace or None: Race where user had his record
        """
        race_to_search = self.my_finished_races.filter(race_id__type=race_type)
        if not race_to_search:
            return None
        best_race = race_to_search[0]
        for race in race_to_search:
            if race.time <= best_race.time:
                best_race = race
        return best_race

    def get_pb_for_race_len(self, race_len):
        """Return user PB for race length, None if not ran this race type.

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
            dict: Stats `km`, `races`, `favourite` race type
        """
        km_ram = 0
        races_finished = self.my_finished_races.count()
        most_common_race_len = Race.objects.filter(userraces__profile_id=self).\
            values_list('length').\
            annotate(race_len_counter=Count('length')).\
            order_by('-race_len_counter')
        if most_common_race_len:
            favourite_race_type = get_type_from_length(most_common_race_len[0][0])
        else:
            favourite_race_type = None
        for race in self.my_finished_races:
            km_ram += race.race_id.length

        result = {"km": km_ram, "races": races_finished, "favourite": favourite_race_type}

        return result

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()


class UserRaces(models.Model):
    """Represent race which user wants to run."""
    profile_id = models.ForeignKey(Profile, on_delete=models.CASCADE, default=1)
    race_id = models.ForeignKey(Race, on_delete=models.CASCADE, default=1)
    time = models.IntegerField(verbose_name="Race time in seconds", default=0)
    finished = models.BooleanField(verbose_name="If user finished race", default=False)

    def __gt__(self, other):
        if self.race_id.date > other.race_id.date:
            return self

    def __lt__(self, other):
        if self.race_id.date < other.race_id.date:
            return other

    def __str__(self):
        return f"{self.profile_id.first_name} -- {self.race_id.place} {self.race_id.length}"

    def race_speed(self) -> float:
        """Calculate speed in km/h for race.

        Returns:
            race_speed (float) : Race speed in km/h.
        """
        if self.finished:
            return self.race_id.length / self.time * 3600
        return False

    def race_pace(self):
        """Get pace for current race in min/km.

        Returns:
            dict[int, int, int]: {"hours": h, "minutes": m, "seconds": s}
        """

        if self.finished:
            pace_s_per_km = self.time/self.race_id.length
            return sec_to_human(pace_s_per_km)
        return False


class Trophy(models.Model):
    """Represent trophy with name and condition"""
    name = models.CharField(verbose_name="Name of trophy", max_length=30, default='')
    detail = models.CharField(verbose_name="Description when earn this trophy is earned.", max_length=200)

    # image = models.ImageField()
    # neki spisak uslova
    # progress? broj trenutnih trka vs broj potrebnih trka

    def __str__(self):
        return f"{self.name} - {self.detail}"

    @property
    def classname(obj):
        return obj.__class__.__name__


class UserTrophy(models.Model):
    """Represent when user earns trophy."""
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    trophy = models.ForeignKey(Trophy, on_delete=models.CASCADE)
    date_earned = models.DateField(verbose_name="Date on which user earned trophy", auto_now=True)
    race_earned = models.ForeignKey(verbose_name="Race where user earned trophy", to=Race, on_delete=models.CASCADE,
                                    null=True)

    def __str__(self):
        return f"{self.profile} earned {self.trophy} for {self.race_earned} on {self.date_earned}"

    @property
    def classname(obj):
        return obj.__class__.__name__


class Gear(models.Model):
    shoes = models.CharField(max_length=100) # mozda baza za sve patike
    watch = models.CharField(max_length=100) # mozda baza za sve satove
    shirt_size = models.CharField(choices=SHIRT_SIZE, max_length=50)
    shorts_size = models.CharField(choices=SHORTS_SIZE, max_length=50)


class UserGear(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    gear = models.ForeignKey(Gear, on_delete=models.CASCADE)


class GearForm(ModelForm):
    class Meta:
        model = Gear
        fields = '__all__'


class RaceForm(ModelForm):
    class Meta:
        model = Race
        fields = '__all__'


class UserRaceForm(ModelForm):
    class Meta:
        model = UserRaces
        fields = '__all__'
