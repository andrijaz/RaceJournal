from django.contrib import admin

# Register your models here.
from manager.models import Staff, Group, Training, Member, MemberGroup, OneTrainingPlan, MonthPlan, MonthTrainingPlan

admin.site.register(Group)
admin.site.register(Training)
admin.site.register(Member)
admin.site.register(Staff)
admin.site.register(MemberGroup)
admin.site.register(OneTrainingPlan)
admin.site.register(MonthPlan)
admin.site.register(MonthTrainingPlan)