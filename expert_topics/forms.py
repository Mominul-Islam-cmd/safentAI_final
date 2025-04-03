from django import forms
from .models import ResearchTopic


class ResearchTopicForm(forms.ModelForm):
    class Meta:
        model = ResearchTopic
        fields = ['title', 'subject', 'description', 'category']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
        }


class ResearchTopicApprovalForm(forms.ModelForm):
    class Meta:
        model = ResearchTopic
        fields = ['status']
