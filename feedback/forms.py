from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['title', 'content', 'rating', 'feedback_type']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Feedback Title'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Your Feedback'}),
            'rating': forms.Select(attrs={'class': 'form-control'}),
            'feedback_type': forms.Select(attrs={'class': 'form-control'}),
        }

class FeedbackApprovalForm(forms.ModelForm):
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('approved', 'Approve & Publish'),
        ('rejected', 'Reject')
    ]
    
    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = Feedback
        fields = ['status']