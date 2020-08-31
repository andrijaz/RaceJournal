from manager.models import Member, MonthTrainingPlan, MonthPlan, Training, OneTrainingPlan
from django.forms import ModelForm

class MemberForm(ModelForm):
    class Meta:
        model = Member
        # fields = '__all__'
        exclude = ['profile']


class MonthPlanForm(ModelForm):
    class Meta:
        model = MonthPlan
        fields = '__all__'
        # exclude

class OneTrainingPlanForm(ModelForm):
    class Meta:
        model = OneTrainingPlan
        fields = '__all__'

class TrainingForm(ModelForm):
    class Meta:
        model = Training
        fields = '__all__'