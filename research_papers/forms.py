from django import forms
from .models import ResearchPaper


class ResearchPaperForm(forms.ModelForm):
    class Meta:
        model = ResearchPaper
        fields = ['title', 'co_authors', 'abstract', 'paper_link', 'category']
        widgets = {
            'abstract': forms.Textarea(attrs={'rows': 5}),
        }


class ResearchPaperApprovalForm(forms.ModelForm):
    class Meta:
        model = ResearchPaper
        fields = ['status']
