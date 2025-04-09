from django import forms
from PublicationProject.models import Publication,Project

class Publication_form(forms.ModelForm):
    class Meta:
        model=Publication
        fields= "__all__"

# class publication_details(forms.ModelForm):
#     class Meta:
#         model=publication_details
#         fields= "__all__"


# Project

class Project_form(forms.ModelForm):
    class Meta:
        model=Project
        fields= "__all__"