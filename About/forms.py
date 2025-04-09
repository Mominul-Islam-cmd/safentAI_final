from django import forms
from About.models import TeamMembers

class team_form_Details(forms.ModelForm):
    class Meta:
        model=TeamMembers
        fields= "__all__"
