from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from .models import Profile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ProfileRegisterForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['institution_name', 'profile_picture', 'phone_number']
        widgets = {
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'institution_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your institution name'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your phone number'})
        }
        
    def clean_profile_picture(self):
        profile_picture = self.cleaned_data.get('profile_picture')
        if profile_picture:
            # 256KB = 262,144 bytes
            if profile_picture.size > 262144:
                raise forms.ValidationError("Profile picture must be less than 256KB in size.")
        return profile_picture


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['institution_name', 'profile_picture', 'phone_number']
        
    def clean_profile_picture(self):
        profile_picture = self.cleaned_data.get('profile_picture')
        if profile_picture:
            # 256KB = 262,144 bytes
            if profile_picture.size > 262144:
                raise forms.ValidationError("Profile picture must be less than 256KB in size.")
        return profile_picture


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    subject = forms.CharField(max_length=200)
    message = forms.CharField(widget=forms.Textarea)


class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'}))
    
    def clean(self):
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        
        if email and password:
            # Find a user with the provided email
            try:
                user = User.objects.get(email=email)
                # Update username field with the found user's username for authentication
                self.cleaned_data['username'] = user.username
            except User.DoesNotExist:
                raise forms.ValidationError("Invalid email or password.")
                
            # Authenticate with the username and password
            user = authenticate(username=self.cleaned_data['username'], password=password)
            if user is None:
                raise forms.ValidationError("Invalid email or password.")
            
        return super().clean()
