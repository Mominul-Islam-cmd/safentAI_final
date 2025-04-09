from django import forms
from Researchers.models import researcher_form,researcher_recommend

class Researcher_form_Details(forms.ModelForm):
    class Meta:
        model=researcher_form
        fields= "__all__"

class researcher_recommend_details(forms.ModelForm):
    class Meta:
        model=researcher_recommend
        fields= "__all__"