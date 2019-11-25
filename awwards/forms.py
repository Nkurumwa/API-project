from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Profile, Project, Rate, Review
from django.contrib.auth.models import User


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_pic', 'bio']


class ProjectPostForm(forms.ModelForm):
    class Meta:
        model=Project
        exclude=['user','design','usability','content']

class RateForm(forms.ModelForm):
    class Meta:
        model = Rate
        exclude = ['user','project']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        exclude = ['user','profile_id']