from race.models import Profile
from django.forms import ModelForm

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        # fields = '__all__'
        exclude = ['user']
