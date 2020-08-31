from django.contrib import admin

# Register your models here.
from race.models import Race, UserRaces, UserTrophy

admin.site.register(Race)
admin.site.register(UserRaces)
admin.site.register(UserTrophy)