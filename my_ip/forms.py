from .models import Profile, Project, Rating
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm, Textarea, IntegerField, EmailField, CharField, Form, ImageField


class ProjectForm(forms.ModelForm):
    photo = ImageField(label='')

    class Meta:
        model = Project
        fields = ('title', 'project_image', 'description', 'live_link', 'github_link')


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['design', 'usability', 'content']


class ProfileForm(forms.Form):
    class Meta:
        model = Profile
        fields = ['profile_pic', 'bio', 'email', 'contact']