from django import forms
from .models import BlogPost


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'category']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 10, 'class': 'medium-editor-textarea'}),
        }


class BlogPostApprovalForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['status']
