from django.db import models
from race.models import Profile, User, Gear
from datetime import datetime
from django.urls import reverse


class Staff(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    role = models.CharField(max_length=50)
    type = models.CharField(max_length=50,
                            choices=[("coach", "coach"), ("manager", "manager"), ("organizer", "organizer")])

    def __str__(self):
        return f"{self.type}, {self.profile.first_name}"

    @property
    def my_members(self):
        return MemberGroup.objects.filter(group__coach__profile=self.profile)

    @property
    def my_groups(self):
        return Group.objects.filter(coach=self)

    def get_absolute_url(self):
        return reverse('staff-detail', kwargs={'pk': self.pk})


class Member(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    # broj godina / semestara
    # neki trofej kao iz RaceApp
    # dodati opremu da trener moze da vidi
    # isto sto i trkac samo drugi pogled i druge informacije?
    goals = models.CharField(max_length=50)
    target_race = models.CharField(max_length=50)
    injuries = models.CharField(max_length=50, blank=True)
    notes = models.CharField(max_length=200, blank=True)

    # financial = plan za placanje?
    # posecenst = models.IntegerField(...)

    def __str__(self):
        return self.profile.first_name

    @property
    def my_group(self):
        return MemberGroup.objects.get(member=self).group

    def get_absolute_url(self):
        return reverse('member-detail', kwargs={'pk': self.pk})


class Group(models.Model):
    name = models.CharField(max_length=50)
    coach = models.ForeignKey(to=Staff, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    @property
    def members(self):
        # MemberGroup.objects.filter(group__name=self.name)
        return MemberGroup.objects.filter(group=self.id)

    @property
    def current_plan(self):
        # return "plan za ovaj mesec"
        mp = MonthPlan.objects.get(group=self, month=datetime.now().month, year=datetime.now().year)
        return MonthTrainingPlan.objects.get(month_plan=mp)
        # return MonthTrainingPlan.objects.filter(group=self)

    @property
    def this_month_plan(self):
        mp = MonthPlan.objects.get(group=self, month=datetime.now().month, year=datetime.now().year)
        return MonthTrainingPlan.objects.filter(month_plan=mp)

    @property
    def all_plans(self):
        return MonthPlan.objects.filter(group=self)

    @property
    def next_training(self):
        mp = MonthPlan.objects.get(group=self, month=datetime.now().month, year=datetime.now().year)
        return MonthTrainingPlan.objects.filter(month_plan=mp).order_by('training')[0]

    def get_absolute_url(self):
        return reverse('group-detail', kwargs={'pk': self.pk})

class MemberGroup(models.Model):
    member = models.ForeignKey(to=Member, on_delete=models.CASCADE)
    group = models.ForeignKey(to=Group, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.member.profile.first_name} - {self.member.goals}"


class MonthPlan(models.Model):
    name = models.CharField(max_length=50)
    month = models.CharField(choices=[(x,x) for x in range(1, 13)], default=datetime.now().month, max_length=10)
    year = models.CharField(choices=[(x,x) for x in range(2015, 2040)], default=datetime.now().year, max_length=10)
    group = models.ForeignKey(to=Group, blank=True, on_delete=models.CASCADE)

    # tip - pon/sre/sub
    # koliko km i sati trcanja
    # koliko u kojoj zoni trcimo

    def __str__(self):
        return f"{self.name}  - {self.month} - {self.group}"

    @property
    def next_training(self):
        # return TrainingPlan.objects.get(pk=1)
        # treba da vrati Trainging objekat a ne TraingingPlan
        # Training.objects.get(plan=self)
        MonthTrainingPlan.objects.get()
        return "PRVI TRENING"


    def get_absolute_url(self):
        return reverse('month-plan-detail', kwargs={'pk': self.pk})

class OneTrainingPlan(models.Model):
    """
        PLan for one specific training.
    """
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=50, choices=[("time", "time"), ("distance", "distance"), ("mixed", "mixed")])
    length = models.CharField(max_length=20)
    # date
    # ukupno vreme ili km
    # intervali
    # trener da popuni meso treninga i ukupno km/vreme on racuna ostalo !!


    def get_absolute_url(self):
        return reverse('one-training-plan-detail', kwargs={'pk': self.pk})


class Training(models.Model):
    location = models.CharField(max_length=50)
    time = models.DateTimeField()
    special = models.CharField(max_length=100, blank=True)  # izlet, lokacija, beleska neka
    name = models.CharField(max_length=50)
    plan = models.ForeignKey(to=OneTrainingPlan, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.location} {self.time.date()}"

    def get_absolute_url(self):
        return reverse('training-detail', kwargs={'pk': self.pk})


class MonthTrainingPlan(models.Model):
    month_plan = models.ForeignKey(to=MonthPlan, on_delete=models.CASCADE)
    training = models.ForeignKey(to=Training, on_delete=models.CASCADE)
    group = models.ForeignKey(to=Group, on_delete=models.CASCADE)

    def next_training(self):
        MonthTrainingPlan.objects.get()

    # def get_absolute_url(self):
    #     return reverse('monthtrainingplan-detail', kwargs={'pk': self.pk})
        # return reverse('month-plan-detail', kwargs={'pk': self.pk})

class Clanarina(models.Model):
    # za koji program?
    # tip - mesecna, semestar
    # popust
    pass


class Posecenost:
    # mozda samo jedan broj u memeber? pa u odnosu na broj dosadasnjih treninga
    pass
